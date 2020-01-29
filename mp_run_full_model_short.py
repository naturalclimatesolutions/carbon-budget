import argparse
import constants_and_names as cn
import universal_util as uu
from gain.mp_forest_age_category_natrl_forest import mp_forest_age_category_natrl_forest
from gain.mp_gain_year_count_natrl_forest import mp_gain_year_count_natrl_forest
from gain.mp_annual_gain_rate_natrl_forest import mp_annual_gain_rate_natrl_forest
from gain.mp_cumulative_gain_natrl_forest import mp_cumulative_gain_natrl_forest
from gain.mp_merge_cumulative_annual_gain_all_forest_types import mp_merge_cumulative_annual_gain_all_forest_types
from carbon_pools.mp_create_carbon_pools import mp_create_carbon_pools
# import mp_calculate_gross_emissions

def main ():

    model_stages = ['all', 'forest_age_category_natrl_forest', 'gain_year_count_natrl_forest',
                    'annual_gain_rate_natrl_forest', 'cumulative_gain_natrl_forest',
                     'removals_merged', 'carbon_pools', 'gross_emissions']


    # The argument for what kind of model run is being done: standard conditions or a sensitivity analysis run
    parser = argparse.ArgumentParser(description='Create tiles of the number of years of carbon gain for mangrove forests')
    parser.add_argument('--model-type', '-t', required=True, help='{}'.format(cn.model_type_arg_help))
    parser.add_argument('--stages', '-s', required=True,
                        help='Stages of creating Brazil legal Amazon-specific gross cumulative removals. Options are {}'.format(model_stages))
    parser.add_argument('--run_through', '-r', required=True,
                        help='Options: true or false. true: run named stage and following stages. false: run only named stage.')
    parser.add_argument('--tile_id_list', '-l', required=True,
                        help='List of tile ids to use in the model. Should be of form 00N_110E or all.')
    parser.add_argument('--carbon-pool-extent', '-ce', required=False,
                        help='Extent over which carbon pools should be calculated: loss or 2000')
    parser.add_argument('--pools-to-use', '-p', required=True,
                        help='Options are soil_only or biomass_soil. Former only considers emissions from soil. Latter considers emissions from biomass and soil.')
    args = parser.parse_args()
    sensit_type = args.model_type
    stage_input = args.stages
    run_through = args.run_through
    carbon_pool_extent = args.carbon_pool_extent
    pools = args.pools_to_use
    tile_id_list = args.tile_id_list


    # Checks whether the sensitivity analysis argument is valid
    uu.check_sensit_type(sensit_type)


    # Checks the validity of the model stage arguments. If either one is invalid, the script ends.
    if (stage_input not in model_stages):
        raise Exception('Invalid stage selection. Please provide a stage from {}.'.format(model_stages))
    else:
        pass
    if (run_through not in ['true', 'false']):
        raise Exception('Invalid run through option. Please enter true or false.')
    else:
        pass


    # Generates the list of stages to run
    actual_stages = uu.analysis_stages(model_stages, stage_input, run_through)
    print actual_stages

    tile_id_list = uu.tile_id_list_check(tile_id_list)


    # List of output directories and output file name patterns
    raw_output_dir_list = [
                       cn.age_cat_natrl_forest_dir, cn.gain_year_count_natrl_forest_dir,
                       cn.annual_gain_AGB_natrl_forest_dir, cn.annual_gain_BGB_natrl_forest_dir,
                       cn.cumul_gain_AGCO2_natrl_forest_dir, cn.cumul_gain_BGCO2_natrl_forest_dir,
                       cn.annual_gain_AGB_BGB_all_types_dir, cn.cumul_gain_AGCO2_BGCO2_all_types_dir,
                       cn.AGC_emis_year_dir, cn.BGC_emis_year_dir, cn.deadwood_emis_year_2000_dir,
                       cn.litter_emis_year_2000_dir, cn.soil_C_emis_year_2000_dir, cn.total_C_emis_year_dir
                       ]

    raw_output_pattern_list = [
                           cn.pattern_age_cat_natrl_forest, cn.pattern_gain_year_count_natrl_forest,
                           cn.pattern_annual_gain_AGB_natrl_forest, cn.pattern_annual_gain_BGB_natrl_forest,
                           cn.pattern_cumul_gain_AGCO2_natrl_forest, cn.pattern_cumul_gain_BGCO2_natrl_forest,
                           cn.pattern_annual_gain_AGB_BGB_all_types, cn.pattern_cumul_gain_AGCO2_BGCO2_all_types,
                           cn.pattern_AGC_emis_year, cn.pattern_BGC_emis_year, cn.pattern_deadwood_emis_year_2000,
                           cn.pattern_litter_emis_year_2000, cn.pattern_soil_C_emis_year_2000, cn.pattern_total_C_emis_year
                           ]


    # If the model run isn't the standard one, the output directory and file names are changed.
    # Otherwise, they stay standard.
    if sensit_type != 'std':
        print "Changing output directory and file name pattern based on sensitivity analysis"
        master_output_dir_list = uu.alter_dirs(sensit_type, raw_output_dir_list)
        master_output_pattern_list = uu.alter_patterns(sensit_type, raw_output_pattern_list)
    else:
        master_output_dir_list = raw_output_dir_list
        master_output_pattern_list = raw_output_pattern_list


    # Creates forest age category tiles
    if 'forest_age_category_natrl_forest' in actual_stages:

        print 'Creating forest age category for natural forest tiles'

        mp_forest_age_category_natrl_forest(sensit_type, tile_id_list)


    # Creates tiles of the number of years of removals
    if 'gain_year_count_natrl_forest' in actual_stages:

        print 'Creating gain year count tiles for natural forest'

        mp_gain_year_count_natrl_forest(sensit_type, tile_id_list)


    # Creates tiles of annual AGB and BGB gain rate for non-mangrove, non-planted forest using the standard model
    # removal function
    if 'annual_gain_rate_natrl_forest' in actual_stages:

        print 'Creating annual removals for natural forest'

        mp_annual_gain_rate_natrl_forest(sensit_type, tile_id_list)


    # Creates tiles of cumulative AGCO2 and BGCO2 gain rate for non-mangrove, non-planted forest using the standard model
    # removal function
    if 'cumulative_gain_natrl_forest' in actual_stages:

        print 'Creating cumulative removals for natural forest'

        mp_cumulative_gain_natrl_forest(sensit_type, tile_id_list)


    # Creates tiles of annual gain rate and cumulative removals for all forest types (above + belowground)
    if 'removals_merged' in actual_stages:

        print 'Creating annual and cumulative removals for all forest types combined (above + belowground)'

        mp_merge_cumulative_annual_gain_all_forest_types(sensit_type, tile_id_list)



    # Creates carbon pools in loss year
    if 'carbon_pools' in actual_stages:

        print 'Creating emissions year carbon pools'

        mp_create_carbon_pools(sensit_type, tile_id_list, carbon_pool_extent)


    if 'gross_emissions' in actual_stages:

        print 'Creating gross emissions tiles'






if __name__ == '__main__':
    main()