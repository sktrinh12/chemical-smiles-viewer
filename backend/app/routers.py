from fastapi import APIRouter, Depends, status
from rdkit.Chem import MolFromSmiles
from rdkit.Chem.Draw import rdMolDraw2D
from starlette.responses import JSONResponse, Response
from wurlitzer import pipes

from app import config, oracle, utils

logger = utils.get_logger(__name__)


def get_smiles(compound_id: str, settings):
    output = None
    try:
        with oracle.OracleConnection(settings.oracle_username,
                                     settings.oracle_password,
                                     settings.oracle_host,
                                     settings.oracle_port,
                                     settings.oracle_sid) as con:
            sql_stmt = f"""SELECT CLOSESTSMILES FROM
                           FOUNT.CALCULATED_FT_VK_QSAR_MODELS
                           WHERE REGNO = '{compound_id}' FETCH
                           NEXT 1 ROWS ONLY"""
            with con.cursor() as cursor:
                cursor.execute(sql_stmt)
                output = cursor.fetchall()
                output = output[0][0]
    except Exception as e:
        msg = f"error running sql query for {compound_id} - {e}"
        logger.exception(msg)
        print(msg)
    return output


smiles_router = APIRouter(prefix="/v1")


@smiles_router.get("/draw-smiles")
async def draw(compound_id: str,
               size: int,
               settings: config.Settings = Depends(config.get_settings)):
    """
    Convert SMILE code to 2D molecule image in SVG format
    :param smiles:
    :param size: width x height of svg figure
    :return:
    """

    try:
        with pipes() as (out, err):
            smiles = get_smiles(compound_id, settings)
            # convert from smiles to molecule class
            molecule = MolFromSmiles(smiles)
        stderr: str = err.read()
        if molecule:
            molecule = rdMolDraw2D.PrepareMolForDrawing(molecule)
            # start drawing molecule image
            drawer = rdMolDraw2D.MolDraw2DSVG(size, size)
            drawer.drawOptions().addStereoAnnotation = True
            # drawer.drawOptions().addAtomIndices = True
            drawer.DrawMolecule(molecule)
            drawer.FinishDrawing()
            # response as proper svg+xml
            svg = drawer.GetDrawingText()
            print({"compound_id": compound_id, "smiles": smiles, "size": size})
            return Response(content=svg, media_type="image/svg+xml")
        else:
            data = {"API Error": stderr.splitlines()[1]}
            return JSONResponse(content=data, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as ex:
        print(ex)
