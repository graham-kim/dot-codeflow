import pyparsing as pp

def cluster_pattern() -> pp.And:
    return pp.Word("/@") \
         + pp.Word(pp.alphanums+"_-")("name") \
         + pp.Optional( # Start of optional labels
              pp.Suppress("|") \
            + pp.Combine(
                  pp.Word(pp.alphas) + "=" + pp.Word(pp.alphanums+'"'+"'") \
                + pp.Optional(pp.Suppress(",")) # Allow comma separation
              )[1,...]("attrs")
          )

def node_pattern() -> pp.And:
    return pp.Char("-") \
         + pp.Word(pp.alphanums+"_-")("name") \
         + pp.Optional( # Start of optional labels
              pp.Suppress("|") \
            + pp.Combine(
                  pp.Word(pp.alphanums+'"'+"'_-@#,.;()[]!?")
              )[1,...]("label")
          )

def link_pattern() -> pp.And:
    return pp.Group( # Start of line
               pp.Char(">") \
             | pp.Combine(pp.Char("<") + pp.Optional(pp.Char(">")))
           )("operator") \
         + pp.Word(pp.alphanums+"_-")("name") \
         + pp.Optional( # Start of optional labels
              pp.Suppress("|") \
            + pp.Combine(
                  pp.Word(pp.alphanums+'"'+"'_-@#,.;()[]!?")
              )[1,...]("label")
          )

def dot_attr_pattern() -> pp.And:
    return pp.Char("=") \
         + pp.Combine(
               pp.Word(pp.alphas) + "=" + pp.Word(pp.alphanums+'"'+"'") \
             + pp.Optional(pp.Suppress(",")) # Allow comma separation
           )[1,...]("attrs")
