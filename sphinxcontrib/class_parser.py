import pyparsing as pp

END = pp.Keyword("end")
LANGLE, RANGLE = map(pp.Literal, "<>")
LPAREN, RPAREN = map(pp.Literal, "()")
CLASSDEF = pp.Keyword("classdef")
PROPERTIES = pp.Keyword("properties")
METHODS = pp.Keyword("methods")
ENUMERATION = pp.Keyword("enumeration")
FUNCTION = pp.Keyword("function")
IF = pp.Keyword("if")
FOR = pp.Keyword("for")
WHILE = pp.Keyword("while")
SWITCH = pp.Keyword("switch")
PERCENT = pp.Literal("%")

# continuation = pp.Literal("...\n").set_parse_action(pp.replace_with("")).leave_whitespace(
control_flow = pp.nested_expr("if", "end") | pp.nested_expr("for", "end") | pp.nested_expr("while", "end") | pp.nested_expr("switch", "end")
value = (pp.quoted_string 
         | pp.original_text_for(pp.Opt(pp.Word(pp.printables, exclude_chars="(),") 
                                     | pp.nested_expr())))
arg_list = LPAREN + pp.DelimitedList(value, combine=True, allow_trailing_delim=True) + RPAREN
func = FUNCTION + pp.Opt(arg_list) + pp.Suppress(control_flow[...]) + END

arg_list_str = """
(1,2,3,)
"""
res = arg_list.parse_string(arg_list_str)
print(res)

control_flow_str = """
if(0)
  while(0)

  end
end
"""
res = control_flow.parse_string(control_flow_str)
print(res)

func_str = """
function()
  if(0)
    while(true)
    end
  end
end
"""
res = func.parse_string(func_str)
print(res)
