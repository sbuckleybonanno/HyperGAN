import tensorflow as tf
import hyperchamber as hc

from hypergan.losses.base_loss import BaseLoss

class SupervisedLoss(BaseLoss):

    def _create(self, d_real, d_fake):
        gan = self.gan
        ops = self.ops
        config = self.config

        batch_size = gan.batch_size()
        net = d_real

        num_classes = ops.shape(gan.inputs.y)[1]
        net = gan.discriminator.ops.linear(net, num_classes)
        net = ops.layer_regularizer(net, config.layer_regularizer, config.batch_norm_epsilon)

        d_class_loss = tf.nn.softmax_cross_entropy_with_logits(logits=net,labels=gan.inputs.y)

        self.metrics = {
            'd_class_loss': d_class_loss
        }

        return [d_class_loss, None]
