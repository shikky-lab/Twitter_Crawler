Twitter���W�X�N���v�g(����)
PYthon3.6�ŏ����܂����D
����Ȃ̂Ńo�O�����X���邩���ł��D�D�D

�d�l
�E�w��L�[���[�h�ł�twitter����(OR�����Ȃǂ̌����ݒ����)
�E�������ʂ����^�f�[�^���݂ŕۑ�(json�`��.API�̌Ăяo�����Ƃɒʂ��ԍ���t���ĘA�ԕۑ�)
�EAPI�����ɂԂ������ꍇ�C���������܂ő҂��Ď����ĊJ�D

�g�p���@
1.Twitter�̃f�x���b�p�[�ɓo�^���āC�A�N�Z�X�g�[�N�������擾
2.Twitter_Crawler.py�Ɠ����f�B���N�g����config.ini�ɃA�N�Z�X�g�[�N���⌟���ݒ���Z�b�g
3.Twitter_Crawler.py�����s�D

config.ini�ɂ���
[tokens]
�A�N�Z�X�g�[�N���Ȃǂ��Z�b�g

[search_params]
�����ݒ���Z�b�g�D�O����TwitterAPI�ɒ��ڃ|�X�g����l�D�����̒l�̈Ӗ��͖{��API�}�j���A�����Q�Ƃ̂��ƁD
�ꕔ���グ���
q:�����N�G���D�����P���AND�����COR�����Ȃǂ��\�D�ڍׂ�API�}�j���A���ցD
since_id:������V�����c�C�[�g�݂̂������ΏۂƂ���D���ݎ擾���Ă���ŐV��tweet��id���Z�b�g���Ď��s����΁C����ȍ~��tweet�̂ݎ擾�ł���D
�Ȃ��C���t�@�����X�ł͂���id���܂܂�����ȍ~��tweet�����W����Ə�����Ă��邪�C�d��������ۂ��̂ŕs���Ȃ�id��1�����Ă������ق����悳���D

�㔼��Twitter_Crawler�Ǝ��̕ϐ��D
search_count:API���Ăяo���񐔁D��{�͐����ȉ��̒l�̃Z�b�g�𐄏��D

[other_settings]
�t�@�C���̕ۑ��ꏊ�Ȃǂ��̑��ݒ�
�Ȃ��C���łɂ��̃p�X�����݂���ꍇ�C���S�̂��ߎ��s�𒆎~����d�l�ɂȂ��Ă���D
save_dir_path:���W���ʂ�ۑ�����f�B���N�g���̈ʒu
save_dir_name:���̃f�B���N�g���̖��O�D�f�t�H���g����[�������[�h]_tweets
