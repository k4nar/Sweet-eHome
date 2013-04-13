from mongokit import Document

class Infos(Document):

    use_dot_notation = True

    structure = {
        'name': basestring,
        'description': basestring,
    }

    def apize(self, root="", shorten=False):
      if shorten:
        return "{}/infos/{}".format(root, self.name)
      return self
