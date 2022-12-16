import string
import argparse

import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F
from img_dataset import ImgDataset

from deep_text_recognition.utils import AttnLabelConverter
from deep_text_recognition.dataset import AlignCollate
from deep_text_recognition.model import Model


'''
- worker           : 데이터 로드에 사용할 PC자원
- batch_size       : 입력되는 데이터의 크기
- saved_model      : 학습된 모델 지정
- batch_max_length : label의 최대 길이, 검출한 text의 최대길이
- imgH             : resize된 이미지의 height
- imgW             : resize된 이미지의 width
- rgb              : rgb 이미지 사용여부, False시 GRAY로 동작
- character        : 검출되는 text 종류
- PAD              : 비율을 유지하면서 이미지 resize 여부
- Transformation   : 변환 모듈 지정 (약인식에서는 TPS사용)
- FeatureExtraction: 특징 추출 모델 지정, 문자인식과 관련된 특징만 추출 (약인식에서는 ResNet사용)
- SequenceModeling : 문맥 인식 모델 지정 (약인식에서는 BiLSTM사용)
- Prediction       : 추출된 특징을 문자로 변환하는 모델 지정 (약인식에서는 Attn사용)
'''

class RecogText:
    def __init__(self):
        self.opt = self.set_parser_argument()
        # 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        self.opt.character = string.printable[:-6]
        self.opt.num_gpu = torch.cuda.device_count()
        
        self.converter = AttnLabelConverter(self.opt.character)
        self.opt.num_class = len(self.converter.character)
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 신경만 초기화
        self.model = Model(self.opt)
        self.model = torch.nn.DataParallel(self.model).to(self.device)

        # 학습된 모델 불러오기
        self.model.load_state_dict(torch.load(self.opt.saved_model, map_location=self.device))
        self.model.eval()
        
    def set_parser_argument(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--workers', type=int, help='number of data loading workers', default=0)
        parser.add_argument('--batch_size', type=int, default=192, help='input batch size')
        parser.add_argument('--saved_model', default='./deeplearning_server/weights/pill_recog_model.pth', required=False, help="path to saved_model to evaluation")
        """ Data processing """
        parser.add_argument('--batch_max_length', type=int, default=25, help='maximum-label-length')
        parser.add_argument('--imgH', type=int, default=32, help='the height of the input image')
        parser.add_argument('--imgW', type=int, default=100, help='the width of the input image')
        parser.add_argument('--rgb', action='store_true', help='use rgb input')
        parser.add_argument('--character', type=str, default='0123456789abcdefghijklmnopqrstuvwxyz', help='character label')
        parser.add_argument('--PAD', action='store_true', help='whether to keep ratio then pad for image resize')
        """ Model Architecture """
        parser.add_argument('--Transformation', default='TPS', type=str, required=False, help='Transformation stage. None|TPS')
        parser.add_argument('--FeatureExtraction', default='ResNet', type=str, required=False, help='FeatureExtraction stage. VGG|RCNN|ResNet')
        parser.add_argument('--SequenceModeling', default='BiLSTM', type=str, required=False, help='SequenceModeling stage. None|BiLSTM')
        parser.add_argument('--Prediction', default='Attn', type=str, required=False, help='Prediction stage. CTC|Attn')
        parser.add_argument('--num_fiducial', type=int, default=20, help='number of fiducial points of TPS-STN')
        parser.add_argument('--input_channel', type=int, default=1, help='the number of input channel of Feature extractor')
        parser.add_argument('--output_channel', type=int, default=512,
                                help='the number of output channel of Feature extractor')
        parser.add_argument('--hidden_size', type=int, default=256, help='the size of the LSTM hidden state')
        
        return parser.parse_args()

    def recog_net(self, opt, device, img_list):
        # 이미지 전처리
        AlignCollate_img = AlignCollate(imgH=opt.imgH, imgW=opt.imgW, keep_ratio_with_pad=opt.PAD)
        # 이미지 전처리 + 데이터셋으로 변환
        image_data = ImgDataset(root=img_list, opt=opt)
        image_loader = torch.utils.data.DataLoader(
            image_data, batch_size=opt.batch_size,
            shuffle=False,
            num_workers=int(opt.workers),
            collate_fn=AlignCollate_img, pin_memory=True)

        pred_text = []
        with torch.no_grad():
            for image_tensors, image_path_list in image_loader:
                batch_size = image_tensors.size(0)
                image = image_tensors.to(device)
                # 인식 가능한 문자의 최대 길이 지정
                length_for_pred = torch.IntTensor([opt.batch_max_length] * batch_size).to(device)
                text_for_pred = torch.LongTensor(batch_size, opt.batch_max_length + 1).fill_(0).to(device)

                # 이미지 내의 text 예측
                preds = self.model(image, text_for_pred, is_train=False)

                # 결과값을 문자에 맞게 변환
                _, preds_index = preds.max(2)
                preds_str = self.converter.decode(preds_index, length_for_pred)
                preds_prob = F.softmax(preds, dim=2)
                preds_max_prob, _ = preds_prob.max(dim=2)
                
                # [s] 토큰으로 문자 단위 분할
                for pred, pred_max_prob in zip(preds_str, preds_max_prob):
                    pred_EOS = pred.find('[s]')
                    pred = pred[:pred_EOS]
                    pred_max_prob = pred_max_prob[:pred_EOS]

                    pred_text.append(pred)
        return pred_text

    def img_text_recog(self, img_list):
        # text 분석
        pill_text = self.recog_net(self.opt, self.device, img_list)
        pill_text.reverse()
        pill_text = "".join(pill_text)
        return pill_text
    
# parser = argparse.ArgumentParser()
# parser.add_argument('--workers', type=int, help='number of data loading workers', default=0)
# parser.add_argument('--batch_size', type=int, default=192, help='input batch size')
# parser.add_argument('--saved_model', default='./deeplearning_server/weights/pill_recog_model.pth', required=False, help="path to saved_model to evaluation")
# """ Data processing """
# parser.add_argument('--batch_max_length', type=int, default=25, help='maximum-label-length')
# parser.add_argument('--imgH', type=int, default=32, help='the height of the input image')
# parser.add_argument('--imgW', type=int, default=100, help='the width of the input image')
# parser.add_argument('--rgb', action='store_true', help='use rgb input')
# parser.add_argument('--character', type=str, default='0123456789abcdefghijklmnopqrstuvwxyz', help='character label')
# parser.add_argument('--PAD', action='store_true', help='whether to keep ratio then pad for image resize')
# """ Model Architecture """
# parser.add_argument('--Transformation', default='TPS', type=str, required=False, help='Transformation stage. None|TPS')
# parser.add_argument('--FeatureExtraction', default='ResNet', type=str, required=False, help='FeatureExtraction stage. VGG|RCNN|ResNet')
# parser.add_argument('--SequenceModeling', default='BiLSTM', type=str, required=False, help='SequenceModeling stage. None|BiLSTM')
# parser.add_argument('--Prediction', default='Attn', type=str, required=False, help='Prediction stage. CTC|Attn')
# parser.add_argument('--num_fiducial', type=int, default=20, help='number of fiducial points of TPS-STN')
# parser.add_argument('--input_channel', type=int, default=1, help='the number of input channel of Feature extractor')
# parser.add_argument('--output_channel', type=int, default=512,
#                         help='the number of output channel of Feature extractor')
# parser.add_argument('--hidden_size', type=int, default=256, help='the size of the LSTM hidden state')
# opt = parser.parse_args()

