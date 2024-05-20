import pyparsing as pp

namechars = pp.alphanums+"_-"

def _optional_label() -> pp.Optional:
    return pp.Optional(
              pp.Suppress("|") \
            + pp.Combine(
                  pp.Word(pp.alphanums+'"'+"'_-=@+*\/%#,.;:<>()[]!?")
              )[1,...]("label")
          )

def grid_pattern() -> pp.And:
    return  pp.Group( # Start of line
               pp.Char(">") \
             | pp.Combine(pp.Char("<") + pp.Optional(pp.Char(">")))
           )("operator") \
         + pp.Combine(
               pp.Char("x") + pp.Word(pp.nums)
           )("x_coord") \
         + pp.Combine(
               pp.Char("y") + pp.Word(pp.nums)
           )("y_coord") \
         + pp.Word(pp.alphanums+".!?")("category") \
         + pp.Word(namechars)("name") \
         + _optional_label()
