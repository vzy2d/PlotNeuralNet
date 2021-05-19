# https://www.overleaf.com/read/nywrxwkmqkbh

import sys
sys.path.append('../')
from pycore.zy import *
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( 'cats.jpg' ),

    # Encoder
    #block-001
    to_ConvConvRelu( name='ccr_b1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="(0,0,0)", width=(2,2), height=40, depth=40  ),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="({}-east)".format('ccr_b1'), width=1, height=40, depth=40, opacity=0.5),
    
    #block-002
    to_ConvConvRelu( name='ccr_b2', s_filer=500, n_filer=(64,64), offset="(1,0,0)", to="({}-east)".format('pool_b1'), width=(2,2), height=36, depth=36  ),
    to_Pool(name="pool_b2", offset="(0,0,0)", to="({}-east)".format('ccr_b2'), width=1, height=36, depth=36, opacity=0.5),
    
    #block-003
    to_ConvConvRelu( name='ccr_b3_0', s_filer=500, n_filer=(64,64), offset="(1,0,0)", to="({}-east)".format('pool_b2'), width=(2,2), height=32, depth=32  ),
    to_ConvConvRelu( name='ccr_b3_1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('ccr_b3_0'), width=(2,2), height=32, depth=32  ),
    to_Pool(name="pool_b3", offset="(0,0,0)", to="({}-east)".format('ccr_b3_1'), width=1, height=32, depth=32, opacity=0.5),

    #block-004
    to_ConvConvRelu( name='ccr_b4_0', s_filer=500, n_filer=(64,64), offset="(1,0,0)", to="({}-east)".format('pool_b3'), width=(2,2), height=28, depth=28  ),
    to_ConvConvRelu( name='ccr_b4_1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('ccr_b4_0'), width=(2,2), height=28, depth=28  ),
    to_Pool(name="pool_b4", offset="(0,0,0)", to="({}-east)".format('ccr_b4_1'), width=1, height=28, depth=28, opacity=0.5),
    
    #block-005
    to_ConvConvRelu( name='ccr_b5', s_filer=500, n_filer=(64,64), offset="(1,0,0)", to="({}-east)".format('pool_b4'), width=(2,2), height=24, depth=24  ),
    to_Pool(name="pool_b5", offset="(0,0,0)", to="({}-east)".format('ccr_b5'), width=1, height=24, depth=24, opacity=0.5),
    

    # Decoder
    #block-005
    to_UnPool(name='unpool_b5', offset="(2,0,0)", to="({}-east)".format('pool_b5'), width=1, height=24, depth=24, opacity=0.5 ),
    to_connection( "pool_b5", "unpool_b5"),
    to_ConvConvRelu( name='unccr_b5', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('unpool_b5'), width=(2,2), height=24, depth=24  ),
    to_skip( of='pool_b5', to='unpool_b5', pos=1.25),

    #block-004
    to_UnPool(name='unpool_b4', offset="(1,0,0)", to="({}-east)".format('unccr_b5'), width=1, height=28, depth=28, opacity=0.5 ),
    to_ConvConvRelu( name='unccr_b4_0', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('unpool_b4'), width=(2,2), height=28, depth=28  ),
    to_ConvConvRelu( name='unccr_b4_1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('unccr_b4_0'), width=(2,2), height=28, depth=28  ),
    to_skip( of='pool_b4', to='unpool_b4', pos=1.25),
    
    #block-003
    to_UnPool(name='unpool_b3', offset="(1,0,0)", to="({}-east)".format('unccr_b4_1'), width=1, height=32, depth=32, opacity=0.5 ),
    to_ConvConvRelu( name='unccr_b3_0', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('unpool_b3'), width=(2,2), height=32, depth=32  ),
    to_ConvConvRelu( name='unccr_b3_1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('unccr_b3_0'), width=(2,2), height=32, depth=32  ),
    to_skip( of='pool_b3', to='unpool_b3', pos=1.25),
    
    #block-002
    to_UnPool(name='unpool_b2', offset="(1,0,0)", to="({}-east)".format('unccr_b3_1'), width=1, height=36, depth=36, opacity=0.5 ),
    to_ConvConvRelu( name='unccr_b2', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('unpool_b2'), width=(2,2), height=36, depth=36  ),
    to_skip( of='pool_b2', to='unpool_b2', pos=1.25),
    
    #block-001
    to_UnPool(name='unpool_b1', offset="(1,0,0)", to="({}-east)".format('unccr_b2'), width=1, height=40, depth=40, opacity=0.5 ),
    to_ConvConvRelu( name='unccr_b1', s_filer=500, n_filer=(64,64), offset="(0,0,0)", to="({}-east)".format('unpool_b1'), width=(2,2), height=40, depth=40  ),
    to_skip( of='pool_b1', to='unpool_b1', pos=1.25),
    
    to_ConvSoftMax( name="soft1", s_filer=512, offset="(0.5,0,0)", to="(unccr_b1-east)", width=1, height=40, depth=40, caption="" ),

    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
