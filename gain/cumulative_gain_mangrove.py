### This script calculates the cumulative above and belowground carbon dioxide gain in mangrove forest pixels from 2001-2015.
### It multiplies the annual biomass gain rate by the number of years of gain by the biomass-to-carbon conversion and
### by to the C to CO2 conversion.

import datetime
import subprocess
import sys
sys.path.append('../')
import constants_and_names as cn
import universal_util as uu

# Calculates cumulative aboveground carbon dioxide gain in mangroves
def cumulative_gain_AGCO2(tile_id, pattern, sensit_type):

    print "Calculating cumulative aboveground CO2 gain:", tile_id

    # Start time
    start = datetime.datetime.now()

    print pattern

    # Creates input file names differently depending on whether it's a sensitivity analysis run or not
    if pattern != 'std':
        print "it's not standard"
        gain_rate_AGB = '{0}_{1}_{2}.tif'.format(tile_id, cn.pattern_annual_gain_AGB_mangrove, sensit_type)
        gain_year_count = '{0}_{1}_{2}.tif'.format(tile_id, cn.pattern_gain_year_count_mangrove, sensit_type)
    else:
        print "it's standard"
        # Names of the annual gain rate and gain year count tiles
        gain_rate_AGB = '{0}_{1}.tif'.format(tile_id, cn.pattern_annual_gain_AGB_mangrove)
        gain_year_count = '{0}_{1}.tif'.format(tile_id, cn.pattern_gain_year_count_mangrove)

    # Carbon gain uses special mangrove biomass:carbon ratio
    accum_calc = '--calc=A*B*{0}*{1}'.format(cn.biomass_to_c_mangrove, cn.c_to_co2)
    AGCO2_accum_outfilename = '{0}_{1}.tif'.format(tile_id, pattern)
    AGCO2_accum_outfilearg = '--outfile={}'.format(AGCO2_accum_outfilename)
    cmd = ['gdal_calc.py', '-A', gain_rate_AGB, '-B', gain_year_count, accum_calc, AGCO2_accum_outfilearg, '--NoDataValue=0', '--overwrite', '--co', 'COMPRESS=LZW']
    subprocess.check_call(cmd)

    # Prints information about the tile that was just processed
    uu.end_of_fx_summary(start, tile_id, pattern)


# Calculates cumulative belowground carbon dioxide gain in mangroves
def cumulative_gain_BGCO2(tile_id, pattern, sensit_type):

    print "Calculating cumulative belowground CO2 gain:", tile_id

    # Start time
    start = datetime.datetime.now()

    # Creates input file names differently depending on whether it's a sensitivity analysis run or not
    if pattern != 'std':
        gain_rate_BGB = '{0}_{1}_{2}.tif'.format(tile_id, cn.pattern_annual_gain_BGB_mangrove, sensit_type)
        gain_year_count = '{0}_{1}_{2}.tif'.format(tile_id, cn.pattern_gain_year_count_mangrove, sensit_type)
    else:
        # Names of the annual gain rate and gain year count tiles
        gain_rate_BGB = '{0}_{1}.tif'.format(tile_id, cn.pattern_annual_gain_BGB_mangrove)
        gain_year_count = '{0}_{1}.tif'.format(tile_id, cn.pattern_gain_year_count_mangrove)

    # Carbon gain uses special mangrove biomass:carbon ratio
    accum_calc = '--calc=A*B*{0}*{1}'.format(cn.biomass_to_c_mangrove, cn.c_to_co2)
    BGCO2_accum_outfilename = '{0}_{1}.tif'.format(tile_id, pattern)
    BGCO2_accum_outfilearg = '--outfile={}'.format(BGCO2_accum_outfilename)
    cmd = ['gdal_calc.py', '-A', gain_rate_BGB, '-B', gain_year_count, accum_calc, BGCO2_accum_outfilearg, '--NoDataValue=0', '--overwrite', '--co', 'COMPRESS=LZW']
    subprocess.check_call(cmd)

    # Prints information about the tile that was just processed
    uu.end_of_fx_summary(start, tile_id, pattern)