import hyperchamber as hc
from hyperchamber import Config
from hypergan.ops import TensorflowOps
from hypergan.gan_component import ValidationException, GANComponent

import hypergan as hg

class BaseGAN(GANComponent):
    def __init__(self, config=None, inputs=None, device='/cpu:0', ops_config=None, ops_backend=TensorflowOps):
        """ Initialized a new GAN."""
        self.inputs = inputs
        self.device = device
        self.ops_backend = ops_backend
        self.ops_config = ops_config
        self.created = False
        self.components = []

        if config == None:
            config = hg.Configuration.default()

        # A GAN as a component has a parent of itself
        # gan.gan.gan.gan.gan.gan
        GANComponent.__init__(self, self, config)

    def batch_size(self):
        #TODO how does this work with generators outside of discriminators?
        if self.inputs == None:
            raise ValidationException("gan.batch_size() requested but no inputs provided")
        return self.ops.shape(self.inputs.x)[0]

    def channels(self):
        #TODO same issue with batch_size
        if self.inputs == None:
            raise ValidationException("gan.channels() requested but no inputs provided")
        return self.ops.shape(self.inputs.x)[-1]

    def width(self):
        #TODO same issue with batch_size
        if self.inputs == None:
            raise ValidationException("gan.width() requested but no inputs provided")
        print("----", self.ops.shape(self.inputs.x))
        return self.ops.shape(self.inputs.x)[2]

    def height(self):
        #TODO same issue with batch_size
        if self.inputs == None:
            raise ValidationException("gan.height() requested but no inputs provided")
        return self.ops.shape(self.inputs.x)[1]

    def get_config_value(self, symbol):
        if symbol in self.config:
            config = hc.Config(hc.lookup_functions(self.config[symbol]))
            return config
        return None

    def create_component(self, defn):
        if defn == None:
            return None
        if defn['class'] == None:
            raise ValidationException("Component definition is missing '" + name + "'")
        print("defn", defn)
        gan_component = defn['class'](self, defn)
        self.components.append(gan_component)
        return gan_component

    def create(self):
        if self.created:
            raise ValidationException("gan.create already called. Cowardly refusing to create graph twice")
        self.created = True

