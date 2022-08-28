import pyparsing as pp

def _optional_label() -> pp.Optional:
    return pp.Optional(
              pp.Suppress("|") \
            + pp.Combine(
                  pp.Word(pp.alphanums+'"'+"'_-@#,.;()[]!?")
              )[1,...]("label")
          )

def cluster_pattern() -> pp.And:
    return pp.Word("/@") \
         + pp.Word(pp.alphanums+"_-")("name") \
         + _optional_label()

def node_pattern() -> pp.And:
    return pp.Char("-") \
         + pp.Word(pp.alphanums+"_-")("name") \
         + _optional_label()

def link_pattern() -> pp.And:
    return pp.Group( # Start of line
               pp.Char(">") \
             | pp.Combine(pp.Char("<") + pp.Optional(pp.Char(">")))
           )("operator") \
         + pp.Word(pp.alphanums+"_-")("name") \
         + _optional_label()

def dot_attr_pattern() -> pp.And:
    return pp.Char("=") \
         + pp.Combine(
               pp.Word(pp.alphas) + "=" \
             + (pp.Word(pp.alphanums) | pp.quotedString) \
             + pp.Optional(pp.Suppress(",")) # Allow comma separation
           )[1,...]("attrs")
