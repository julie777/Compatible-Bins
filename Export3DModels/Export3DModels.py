#Author-Julie Jones
#Description-Export 3D models files for all sizes of bins for all systems

import os
import sys
import traceback
from unicodedata import name

import adsk.cam
import adsk.core
import adsk.fusion

SYSTEMS = ["HarborFreight", "Stanley", ]
P_NAMES = ['_bin_height', '_bin_taper', '_x_unit_size', '_y_unit_size']
S_INFO = {'HarborFreight': {
                        # standard sizes
                'sizes':((1,1), (1,2), (2,2),
                        # additional sizes
                        (2,1), (3,1), (3, 2)),
},
'Stanley': {
                        # standard sizes
                'sizes':((1,1), (1,2), (2,2),
                        # additional sizes
                        (2,1), (3,1), (3, 2)),
}
}

P_SIZE = ['x_units', 'y_units']
# so all the Fusion objects don't have to be passed around
GV = {'ui': None, 'app': None, 'design': None, 'exportmgr': None}


def run(context):
    # get the script location
    GV['scriptdir'] = os.path.dirname(os.path.realpath(__file__))
    GV['ui'] = None

    try:
        prepare_fusion()
        bin_body = prepare_model()

        # ui.messageBox('current dir %s' % os.getcwd())
        for sysname in SYSTEMS:
            set_system_info(sysname)
            # save each size
            for sizes in S_INFO[sysname]['sizes']:
                set_sizes(*sizes)
                save(bin_body, sysname, *sizes)
    except:
        if GV['ui']:
            GV['ui'].messageBox('Failed:\n{}'.format(traceback.format_exc()))
    GV['ui'].messageBox('Done')

def prepare_fusion():
    GV['app'] = adsk.core.Application.get()
    GV['ui'] = GV['app'].userInterface


def prepare_model():
    GV['design'] = GV['app'].activeProduct
    # TODO: validate design name
    GV['exportmgr'] = GV['design'].exportManager
    allComps = GV['design'].allComponents
    for comp in allComps:
        if comp.name == 'Compatible Bin V1':
            break
    else:
        assert False, 'comp not found'

    for body in comp.bRepBodies:
        if body.name == 'bin':
            return body
    else:
        assert False, 'body not found'


def set_system_info(sysname):
    for name in P_NAMES:
        pname = 's' + name
        vname = sysname + name
        pparam = GV['design'].allParameters.itemByName(pname)
        pparam.expression = vname


def set_sizes(x_units, y_units):
    GV['design'].allParameters.itemByName('x_units').expression = str(x_units)
    GV['design'].allParameters.itemByName('y_units').expression = str(y_units)


def save(bin_body, sysname, x, y):
    filename = os.path.join(GV['scriptdir'], '..', sysname, '%sx%s bin.3mf' % (x, y))
    # GV['ui'].messageBox('saving %s %sx%s to %s' % (sysname, x, y, filename))
    # Let the view have a chance to paint just so you can watch the progress.
    # adsk.doEvents()

    exportmgr = GV['design'].exportManager
    # export the root component to printer utility
    exportoptions = exportmgr.createC3MFExportOptions (bin_body, filename)

    exportmgr.execute(exportoptions)


    # # Construct the output filename.
    # filename = f'{folder}\\LensCapHolder_D{Diam_set}mm_Strap_{Width_set}mm.stl'

    # # Save the file as STL.
    # exportMgr = adsk.fusion.ExportManager.cast(design.exportManager)
    # stlOptions = exportMgr.createSTLExportOptions(rootComp)
    # stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
    # stlOptions.filename = filename
    # exportMgr.execute(stlOptions)



    # for param in design.allParameters:
#             try:
#                 paramUnit = param.unit
#             except:
#                 paramUnit = ""
#         # update the values of existing parameters
#             paramInModel = design.allParameters.itemByName(nameOfParam)
#             #paramInModel.unit = unitOfParam
#             paramInModel.expression = expressionOfParam
#             paramInModel.comment = commentOfParam
#             print("Updated {}".format(nameOfParam))