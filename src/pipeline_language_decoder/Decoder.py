from lark import Lark, Transformer
from processor.Processor import Processor
import Preconditions as p
## Decoder
#
# This object is the decoder of the Minisoap that will translate user's instructions into processor commands
class Decoder(Transformer):
    
    ## Grammar of decoder
    #
    # Grammar format from Lark library
    # Describes the language in a format called EBNF
    # rule_name : list of rules and TERMINALS to match
    # TERMINAL: string or a regular expression
    grammar = Lark(r"""
    
    instruction: op args | control_op
    
    control_op: CONTROL
    
    op: OP
    args: "["arg* ("," arg)*"]"
    
    arg: string | floating | integer 
    string: ESCAPED_STRING
    integer: SIGNED_NUMBER
    floating: SIGNED_FLOAT
    
    CONTROL: "stop" | "execute" | "reset" | "tracks" | "streams" | "show" | "help"
    
    OP: "open" | "close" | "read" | "write" | "free" | "record" | "stop_record" | "play" | "stop_play" 
      | "sine" | "constant" | "silence"
      | "nullify" | "fade" | "fadeinv" | "amplitude"
      | "crossfade" | "stereo" | "mix"
    
    
    %import common.ESCAPED_STRING
    %import common.SIGNED_FLOAT
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
    
    
    """, start = "instruction")
    
    
    ## Decoder constructor
    #
    #  @param self Object's pointer
    #  @param processor Minisoap's processor pointer
    def __init__(self, processor):
        
        p.check_instance(processor, Processor, details="Processor given not instance of processor")
        self.p = processor
    
        self.op_d = {
                "open" : self.p.openn,
                "close" : self.p.close,
                "read" : self.p.read,
                "write" : self.p.write,
                "free" : self.p.free,
                "record" : self.p.record,
                "stop_record" : self.p.stop_record,
                "play" : self.p.play,
                "stop_play" : self.p.stop_play,
                
                "sine" : self.p.sine,
                "constant" : self.p.constant,
                "silence" : self.p.silence,
                
                "nullify" : self.p.nullify,
                "fade" : self.p.fade,
                "fadeinv" : self.p.fadeinv,
                "amplitude" : self.p.amplitude,
                
                "crossfade" : self.p.crossfade,
                "stereo" : self.p.stereo,
                "mix" : self.p.mix,
                
                
                "stop": self.p.stop,
                "execute": self.p.execute,
                "reset": self.p.reset,
                "tracks" : self.p.tracks,
                "streams": self.p.streams,
                "show" : self.p.show,
                "help" : self.p.helpp
        }
        
        self.current_op = None
    
    ## @var p
    #  Minisoap's processor pointer
    
    ## @var op_d
    #  Dictionary containing decoder's dispacher for user's instructions
    
    ## @var current_op
    #  Tuple storing current instruction's args
    
    ## Instruction rule decoder
    #
    #  @param self Object's pointer
    #  @param x The Token
    def instruction(self, x):
        return list(x)
    
    ## op decoder
    #
    #  @param self Object's pointer
    #  @param x The Token
    #
    # Calls the processor's corresponding method for operations
    def op(self, x):
        (x,) = x
        self.current_op = self.op_d.get(str(x))
        return str(x)
    
    ## control_op decoder
    #
    #  @param self Object's pointer
    #  @param x The Token
    #
    # Calls the processor's corresponding method for control operations
    def control_op(self, x):
        (x,) = x
        self.op_d.get(str(x))()
        
    ## args rule decoder
    #
    #  @param self Object's pointer
    #  @param x The Token
    #
    # Save the arguments of the instruction
    def args(self, x):
        self.p.add(self.current_op, tuple(x))
        return tuple(x)
    
    
    ## arg rule decoder
    #
    #  @param self Object's pointer
    #  @param x The Token
    def arg(self, x):
        (x,) = x
        return x
    
    ## string TERMINAL decoder
    #
    #  @param self Object's pointer
    #  @param s The Token
    def string(self, s):
        (s,) = s
        return s[1:-1]
    
    ## int TERMINAL decoder
    #
    #  @param self Object's pointer
    #  @param s The Token
    def integer(self, s):
        (s,) = s
        return int(s)
    
    ## floats TERMINAL decoder
    #
    #  @param self Object's pointer
    #  @param s The Token
    def floating(self, s):
        (s,) = s
        return float(s)
    



