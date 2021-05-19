
import sys
sys.path.append('../')
from pycore.zy import *
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('./'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( 'cats.jpg' ), #[width=9cm,height=9cm]

    # ResNet-50
    #block-001
    to_Conv( name='conv_b1', s_filer=112, n_filer=64, offset="(0,0,0)", to="(0,0,0)", width=2, height=45, depth=45, caption="Conv1"),
    
    #block-002
    to_Conv( name='conv_b2', s_filer=56, n_filer=256, offset="(0.5,0,0)", to="({}-east)".format('conv_b1'), width=4, height=28, depth=28, caption="Conv2x"),
    
    #block-003
    to_Conv( name='conv_b3', s_filer=28, n_filer=512, offset="(0.5,0,0)", to="({}-east)".format('conv_b2'), width=8, height=14, depth=14, caption="Conv3x"),

    #block-004
    to_Conv( name='conv_b4', s_filer=14, n_filer=1024, offset="(0.5,0,0)", to="({}-east)".format('conv_b3'), width=16, height=7, depth=7, caption="Conv4x"),
    
    #block-005
    to_Conv( name='conv_b5', s_filer=7, n_filer=512, offset="(0.5,0,0)", to="({}-east)".format('conv_b4'), width=10, height=7, depth=7, caption="Conv5x"),
    
    # SSD
    to_Conv( name='ssd_b1', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('conv_b5'), width=2, height=6.5, depth=6.5, caption=""),
    to_Conv( name='ssd_b2', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('ssd_b1'), width=2, height=5.5, depth=5.5, caption=""),
    to_Conv( name='ssd_b3', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('ssd_b2'), width=2, height=4.75, depth=4.75, caption=""),
    to_Conv( name='ssd_b4', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('ssd_b3'), width=2, height=4, depth=4, caption=""),
    to_Conv( name='ssd_b5', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('ssd_b4'), width=2, height=3.5, depth=3.5, caption=""),

    # DeConv
    to_Sum("Sum1", offset="(1,0,0)", to="({}-east)".format('ssd_b5'), radius=1.5, opacity=0.6),
    to_connection("ssd_b5", "Sum1"),

    to_Conv( name='deconv_b5', s_filer=7, n_filer=2048, offset="(0.75,0,0)", to="({}-east)".format('Sum1'), width=2, height=3.5, depth=3.5, caption=""),
    to_connection("Sum1", "deconv_b5"),
    
    to_Sum("Sum2", offset="(0.75,0,0)", to="({}-east)".format('deconv_b5'), radius=1.5, opacity=0.6),
    to_connection("deconv_b5", "Sum2"),

    to_Conv( name='deconv_b4', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('Sum2'), width=2, height=4, depth=4, caption=""),
    to_connection("Sum2", "deconv_b4"),
    
    to_Sum("Sum3", offset="(0.75,0,0)", to="({}-east)".format('deconv_b4'), radius=1.5, opacity=0.6),
    to_connection("deconv_b4", "Sum3"),

    to_Conv( name='deconv_b3', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('Sum3'), width=2, height=4.75, depth=4.75, caption=""),
    to_connection("Sum3", "deconv_b3"),
    
    to_Sum("Sum4", offset="(0.75,0,0)", to="({}-east)".format('deconv_b3'), radius=1.5, opacity=0.6),
    to_connection("deconv_b3", "Sum4"),

    to_Conv( name='deconv_b2', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('Sum4'), width=2, height=5.5, depth=5.5, caption=""),
    to_connection("Sum4", "deconv_b2"),
    
    to_Sum("Sum5", offset="(0.75,0,0)", to="({}-east)".format('deconv_b2'), radius=1.5, opacity=0.6),
    to_connection("deconv_b2", "Sum5"),

    to_Conv( name='deconv_b1', s_filer=7, n_filer=2048, offset="(0.5,0,0)", to="({}-east)".format('Sum5'), width=2, height=6.5, depth=6.5, caption=""),
    to_connection("Sum5", "deconv_b1"),
    
    to_skip( of='conv_b3', to='Sum5', pos=1.25),
    to_skip( of='ssd_b1', to='Sum4', pos=1.25),
    to_skip( of='ssd_b2', to='Sum3', pos=1.25),
    to_skip( of='ssd_b3', to='Sum2', pos=1.25),
    to_skip( of='ssd_b4', to='Sum1', pos=1.25),

    to_connection("conv_b5", "ssd_b1"),
    to_connection("ssd_b1", "ssd_b2"),
    to_connection("ssd_b2", "ssd_b3"),
    to_connection("ssd_b3", "ssd_b4"),
    to_connection("ssd_b4", "ssd_b5"),
    
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
