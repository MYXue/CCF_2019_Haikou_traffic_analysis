# -*- coding: utf-8 -*
"""
2019-11-24
pyecharts 画地图的时候一些风格的控制
"""

def get_map_style():
    map_style = {
                "styleJson": [
                    {
                        "featureType": "water",
                        "elementType": "all",
                        "stylers": {"color": "#696969"},
                    },
                    {
                        "featureType": "land",
                        "elementType": "geometry",
                        "stylers": {"color": "#CFCFCF"},
                    },
                    # {
                    #     "featureType": "highway",
                    #     "elementType": "all",
                    #     "stylers": {"visibility": "off"},
                    # },
                    # {
                    #     "featureType": "arterial",
                    #     "elementType": "geometry.fill",
                    #     "stylers": {"color": "#000000"},
                    # },
                    # {
                    #     "featureType": "arterial",
                    #     "elementType": "geometry.stroke",
                    #     "stylers": {"color": "#0b3d51"},
                    # },
                    # {
                    #     "featureType": "local",
                    #     "elementType": "geometry",
                    #     "stylers": {"color": "#000000"},
                    # },
                    # {
                    #     "featureType": "railway",
                    #     "elementType": "geometry.fill",
                    #     "stylers": {"color": "#000000"},
                    # },
                    # {
                    #     "featureType": "railway",
                    #     "elementType": "geometry.stroke",
                    #     "stylers": {"color": "#08304b"},
                    # },
                    # {
                    #     "featureType": "subway",
                    #     "elementType": "geometry",
                    #     "stylers": {"lightness": -70},
                    # },
                    # {
                    #     "featureType": "building",
                    #     "elementType": "geometry.fill",
                    #     "stylers": {"color": "#000000"},
                    # },
                    # {
                    #     "featureType": "all",
                    #     "elementType": "labels.text.fill",
                    #     "stylers": {"color": "#857f7f"},
                    # },
                    # {
                    #     "featureType": "all",
                    #     "elementType": "labels.text.stroke",
                    #     "stylers": {"color": "#000000"},
                    # },
                    # {
                    #     "featureType": "building",
                    #     "elementType": "geometry",
                    #     "stylers": {"color": "#022338"},
                    # },
                    # {
                    #     "featureType": "green",
                    #     "elementType": "geometry",
                    #     "stylers": {"color": "#062032"},
                    # },
                    # {
                    #     "featureType": "boundary",
                    #     "elementType": "all",
                    #     "stylers": {"color": "#465b6c"},
                    # },
                    # {
                    #     "featureType": "manmade",
                    #     "elementType": "all",
                    #     "stylers": {"color": "#022338"},
                    # },
                    # {
                    #     "featureType": "label",
                    #     "elementType": "all",
                    #     "stylers": {"visibility": "off"},
                    # },
                ]
            }
    return map_style