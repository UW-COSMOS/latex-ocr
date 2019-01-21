from scipy.misc import imread
import PIL
from PIL import Image


from model.img2seq import Img2SeqModel
from model.utils.general import Config, run
from model.utils.text import Vocab
from model.utils.image import greyscale, crop_image, pad_image, \
    downsample_image, TIMEOUT



def img2latex(model, img_path):

    if img_path[-3:] == "png":
        img = imread(img_path)

    elif img_path[-3:] == "pdf":
        # call magick to convert the pdf into a png file
        buckets = [
        [240, 100], [320, 80], [400, 80], [400, 100], [480, 80], [480, 100],
        [560, 80], [560, 100], [640, 80], [640, 100], [720, 80], [720, 100],
        [720, 120], [720, 200], [800, 100], [800, 320], [1000, 200],
        [1000, 400], [1200, 200], [1600, 200], [1600, 1600]
        ]

        dir_output = "tmp/"
        name = img_path.split('/')[-1].split('.')[0]
        run("magick convert -density {} -quality {} {} {}".format(200, 100,
            img_path, dir_output+"{}.png".format(name)), TIMEOUT)
        img_path = dir_output + "{}.png".format(name)
        crop_image(img_path, img_path)
        pad_image(img_path, img_path, buckets=buckets)
        downsample_image(img_path, img_path, 2)

        img = imread(img_path)


    img = greyscale(img)
    hyps = model.predict(img)

#     model.logger.info(hyps[0])
    
    return hyps[0], hyps[1:]
        
        
        


if __name__ == "__main__":
    # restore config and model
    dir_output = "results/full/"
    config_vocab = Config(dir_output + "vocab.json")
    config_model = Config(dir_output + "model.json")
    vocab = Vocab(config_vocab)

    model = Img2SeqModel(config_model, dir_output, vocab)
    model.build_pred()
    model.restore_session(dir_output + "model.weights/")

#     interactive_shell(model)
