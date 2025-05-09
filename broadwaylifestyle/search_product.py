import requests
import json

def search_algolia_index(query):
    url = "https://51css5eb61-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%3B%20instantsearch.js%20(4.63.0)%3B%20Magento2%20integration%20(3.13.4)%3B%20JS%20Helper%20(3.16.1)"
    
    # 注意：URL中已包含x-algolia-agent参数
    # url += "?x-algolia-agent=Algolia%20for%20JavaScript%20(4.14.3)%3B%20Browser%3B%20Magento2%20integration%20(3.13.4)%3B%20autocomplete-core%20(1.7.1)%3B%20autocomplete-js%20(1.7.1)"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded",
        "host": "51css5eb61-dsn.algolia.net",
        "origin": "https://www.broadwaylifestyle.com",
        "referer": "https://www.broadwaylifestyle.com/",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-algolia-api-key": "MTY3MmJiZTg1OTFjMDQ3OTMxN2VhNWRkMzdlN2E2YzgwN2NjNWY0ZTlhNWZlMTcxNTQ4NWE3YzFhOThjODk0ZWZpbHRlcnM9Y2F0YWxvZ19wZXJtaXNzaW9ucy5jdXN0b21lcl9ncm91cF8wKyUyMSUzRCswJnRhZ0ZpbHRlcnM9",
        "x-algolia-application-id": "51CSS5EB61"
    }
    
    try:

        query_params={"requests":[{"indexName":"magento2_live_hk_tc_products","params":"facets=%5B%22H7bo_applicable%22%2C%22H7cl_applicable%22%2C%22H7fa_applicable%22%2C%22a1_camera_TYPE%22%2C%22a1_camera_cmos_type%22%2C%22a2_lenses_TYPE%22%2C%22a2_lenses_format%22%2C%22b1_dehumidifier_capacity%22%2C%22b1_dehumidifier_elg%22%2C%22b2_bathroom_timer%22%2C%22b2_bathroom_tv_min_power%22%2C%22b2_bathroom_tv_remote_control%22%2C%22b2_bathroom_tv_type%22%2C%22b5_energy_label%22%2C%22b5_horsepower%22%2C%22b5_options_remote_control%22%2C%22b5_split_ac_electricty_supply%22%2C%22b5_split_ac_elg%22%2C%22b5_split_ac_horsepower%22%2C%22b5_suggest_coverage_area%22%2C%22b6_built%22%2C%22b6_energy_efficiency_class%22%2C%22b6_inverter%22%2C%22b6_type%22%2C%22b6wc_coolingsystem%22%2C%22b7_21_built_in_new%22%2C%22b7_21_drying_capacity%22%2C%22b7_21_type_new%22%2C%22b7_21_washing_capacity%22%2C%22b7_dw_built_in%22%2C%22b7_dw_washing_capacity_text%22%2C%22b7d_drying_cap%22%2C%22b7wa_washing_capacity%22%2C%22b8_builtin%22%2C%22b8_capacity_filter%22%2C%22b8_hood_type%22%2C%22b8_type_dropdown%22%2C%22b8in_combination%22%2C%22b8in_heat_adjustment%22%2C%22b8twh_hermal_setting%22%2C%22b8twh_type%22%2C%22brand_filter%22%2C%22categories.level0%22%2C%22color%22%2C%22color_filter%22%2C%22energy_efficiency_label%22%2C%22f2sp_radio_function%22%2C%22f6bl_3D%22%2C%22f6bl_resolution%22%2C%22f6bl_wifi%22%2C%22f6bl_wireless%22%2C%22f6dm_light_colour_tone%22%2C%22f6so_sd%22%2C%22f6so_wireless%22%2C%22f6tv_broadway_classify_range%22%2C%22f6tv_record%22%2C%22f6tv_resolution%22%2C%22f6wm_flex%22%2C%22g8_accessories_filter_type%22%2C%22g8_accessories_filter_usage%22%2C%22g8_computer_filter_category%22%2C%22g8_computer_filter_display_size%22%2C%22g8_computer_filter_graphics%22%2C%22g8_computer_filter_memory%22%2C%22g8_computer_filter_memory_speed%22%2C%22g8_computer_filter_operating_system%22%2C%22g8_computer_filter_processor%22%2C%22g8_computer_filter_storagehdd%22%2C%22g8_computer_filter_storagessd%22%2C%22g8_computer_filter_storagetype%22%2C%22g8_computer_filter_touchdisplay%22%2C%22g8_computer_filter_type%22%2C%22g8_computer_filter_weight%22%2C%22g8_consolegaming_filter_category%22%2C%22g8_hmd_filter_platform%22%2C%22g8_luggageandbackpack_filter_size%22%2C%22g8_luggageandbackpack_filter_smartfeature%22%2C%22g8_luggageandbackpack_filter_type%22%2C%22g8_monitor_filter_aspectratio%22%2C%22g8_monitor_filter_displaysize%22%2C%22g8_monitor_filter_flatcurved%22%2C%22g8_monitor_filter_portable%22%2C%22g8_monitor_filter_resolution%22%2C%22g8_monitor_filter_touch%22%2C%22g8_monitor_filter_type%22%2C%22g8_mouseandkeyboard_filter_compatibility%22%2C%22g8_mouseandkeyboard_filter_connectivity%22%2C%22g8_mouseandkeyboard_filter_type%22%2C%22g8_mouseandkeyboard_filter_usage%22%2C%22g8_network_filter_type%22%2C%22g8_network_filter_wifispeed%22%2C%22g8_printer_filter_a3print%22%2C%22g8_printer_filter_autoduplex%22%2C%22g8_printer_filter_colourprint%22%2C%22g8_printer_filter_function%22%2C%22g8_printer_filter_type%22%2C%22g8_projector_filter_type%22%2C%22g8_storage_filter_storage%22%2C%22g8_storage_filter_type%22%2C%22g8_tablets_filter_displayresolution%22%2C%22g8_tablets_filter_displaysize%22%2C%22g8_tablets_filter_network%22%2C%22g8_tablets_filter_phone%22%2C%22g8_tablets_filter_ramsize%22%2C%22g8_tablets_filter_romsize%22%2C%22general_categories%22%2C%22h2ac_type%22%2C%22h2air_suggested_applicable_sq_choice%22%2C%22h2air_type_multiple%22%2C%22h2be_capacity_filter%22%2C%22h2be_coating%22%2C%22h2h5_Pedestal_Desk%22%2C%22h2hc_cold_air_mode%22%2C%22h2hc_effect%22%2C%22h2hc_features%22%2C%22h2hc_foldable_handle%22%2C%22h2he_UPPER_ARM_BLOOD%22%2C%22h2hi_Portable_Steam_Iron%22%2C%22h2in_combination%22%2C%22h2in_heat_adjustment%22%2C%22h2in_power%22%2C%22h2in_top_plate_materials%22%2C%22h2kit_power%22%2C%22h2or_brush_head_qty%22%2C%22h2or_carrying_case%22%2C%22h2rc_capacity_filter%22%2C%22h2rc_inner_material%22%2C%22h2sha_cleaning_system%22%2C%22h2sha_oower%22%2C%22h2sha_quick_charge%22%2C%22h2sha_trimmer%22%2C%22h2sha_washable%22%2C%22h2vc_dust_collect%22%2C%22h2wp_purification%22%2C%22h5_acc_pb_quick_charge_cer%22%2C%22h5_mob_battery_type%22%2C%22h5_mob_bluetooth%22%2C%22h5_mob_gprs%22%2C%22h5_mob_memory_card_max%22%2C%22h5_mob_nfc%22%2C%22h5_mob_ram%22%2C%22h5_mob_rom%22%2C%22h5_mob_share_card_slot%22%2C%22h5_mob_support_dual_sim%22%2C%22h5_s_wearable_clock_display%22%2C%22h5_s_wearable_gps_installed%22%2C%22h5_s_wearable_heart_rate%22%2C%22h5_s_wearable_sim%22%2C%22h5_s_wearable_sleep_tracking%22%2C%22h5_s_wearable_touch_monitor%22%2C%22h5_smartlock_bluetooth%22%2C%22h5_smartlock_card_key%22%2C%22h5_smartlock_fingerprint%22%2C%22h7bo_power%22%2C%22h7cl_power%22%2C%22h7fa_power%22%2C%22manufacturer%22%2C%22price.HKD.default%22%2C%22test_api%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=12&maxValuesPerFacet=10&numericFilters=%5B%22visibility_search%3D1%22%5D&page=0&query=apple&ruleContexts=%5B%22magento_filters%22%5D&tagFilters="}]}
        # 注意：需要将请求体转换为URL编码格式
        response = requests.post(
            url,
            headers=headers,
            json=query_params,  # 直接传递已编码的字符串
            timeout=10,
        )
        print(response)
        if response.status_code == 200:
            data = response.json()
            return data['results'][0]['hits']
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":

    query = "apple"
    result = search_algolia_index(query)
    if result:
        print("请求成功，返回数据：")
        print(result[0])
    else:
        print("请求失败")