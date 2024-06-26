from django.utils.translation import gettext_lazy as _
from collections import namedtuple


Country = namedtuple("Country", ["name", "iso2", "iso3", "uncode"])


COUNTRIES = (      
	Country(_("Afghanistan"), 	                               "AF", 	"AFG", 	  4),
	Country(_("Aland Islands"), 	                           "AX", 	"ALA", 	248),
	Country(_("Albania"), 	                                   "AL", 	"ALB", 	  8),
	Country(_("Algeria"), 	                                   "DZ", 	"DZA", 	 12),
	Country(_("American Samoa"), 	                           "AS", 	"ASM", 	 16),
	Country(_("Andorra"), 	                                   "AD", 	"AND", 	 20),
	Country(_("Angola"), 	                                   "AO", 	"AGO", 	 24),
	Country(_("Anguilla"), 	                                   "AI", 	"AIA", 	660),
	Country(_("Antarctica"), 	                               "AQ", 	"ATA", 	 10),
	Country(_("Antigua and Barbuda"), 	                       "AG", 	"ATG", 	 28),
	Country(_("Argentina"), 	                               "AR", 	"ARG", 	 32),
	Country(_("Armenia"), 	                                   "AM", 	"ARM", 	 51),
	Country(_("Aruba"), 	                                   "AW", 	"ABW", 	533),
	Country(_("Australia"), 	                               "AU", 	"AUS", 	 36),
	Country(_("Austria"), 	                                   "AT", 	"AUT", 	 40),
	Country(_("Azerbaijan"), 	                               "AZ", 	"AZE", 	 31),

	Country(_("Bahamas"), 	                                   "BS", 	"BHS", 	 44),
	Country(_("Bahrain"), 	                                   "BH", 	"BHR", 	 48),
	Country(_("Bangladesh"), 	                               "BD", 	"BGD", 	 50),
	Country(_("Barbados"), 	                                   "BB", 	"BRB", 	 52),
	Country(_("Belarus"), 	                                   "BY", 	"BLR", 	112),
	Country(_("Belgium"), 	                                   "BE", 	"BEL", 	 56),
	Country(_("Belize"), 	                                   "BZ", 	"BLZ", 	 84),
	Country(_("Benin"), 	                                   "BJ", 	"BEN", 	204),
	Country(_("Bermuda"), 	                                   "BM", 	"BMU", 	 60),
	Country(_("Bhutan"), 	                                   "BT", 	"BTN", 	 64),
	Country(_("Bolivia"), 	                                   "BO", 	"BOL", 	 68),
	Country(_("Bosnia and Herzegovina"),                       "BA", 	"BIH", 	 70),
	Country(_("Botswana"), 	                                   "BW", 	"BWA", 	 72),
	Country(_("Bouvet Island"), 	                           "BV", 	"BVT", 	 74),
	Country(_("Brazil"), 	                                   "BR", 	"BRA", 	 76),
	Country(_("British Virgin Islands"),                       "VG", 	"VGB", 	 92),
	Country(_("British Indian Ocean Territory"),               "IO", 	"IOT", 	 86),
	Country(_("Brunei Darussalam"), 	                       "BN", 	"BRN", 	 96),
	Country(_("Bulgaria"), 	                                   "BG", 	"BGR", 	100),
	Country(_("Burkina Faso"), 	                               "BF", 	"BFA", 	854),
	Country(_("Burundi"), 	                                   "BI", 	"BDI", 	108),

	Country(_("Cambodia"), 	                                   "KH", 	"KHM", 	116),
	Country(_("Cameroon"), 	                                   "CM", 	"CMR", 	120),
	Country(_("Canada"), 	                                   "CA", 	"CAN", 	124),
	Country(_("Cape Verde"), 	                               "CV", 	"CPV", 	132),
	Country(_("Cayman Islands"), 	                           "KY", 	"CYM", 	136),
	Country(_("Central African Republic"), 	                   "CF", 	"CAF", 	140),
	Country(_("Chad"), 	                                       "TD", 	"TCD", 	148),
	Country(_("Chile"), 	                                   "CL", 	"CHL", 	152),
	Country(_("China"), 	                                   "CN", 	"CHN", 	156),
	Country(_("Hong Kong, SAR China"), 	                       "HK", 	"HKG", 	344),
	Country(_("Macao, SAR China"), 	                           "MO", 	"MAC", 	446),
	Country(_("Christmas Island"), 	                           "CX", 	"CXR", 	162),
	Country(_("Cocos (Keeling) Islands"), 	                   "CC", 	"CCK", 	166),
	Country(_("Colombia"), 	                                   "CO", 	"COL", 	170),
	Country(_("Comoros"), 	                                   "KM", 	"COM", 	174),
	Country(_("Congo (Brazzaville)"), 	                       "CG", 	"COG", 	178),
	Country(_("Congo, (Kinshasa)"), 	                       "CD", 	"COD", 	180),
	Country(_("Cook Islands"), 	                               "CK", 	"COK", 	184),
	Country(_("Costa Rica"), 	                               "CR", 	"CRI", 	188),
	Country(_("Côte d'Ivoire"), 	                           "CI", 	"CIV", 	384),
	Country(_("Croatia"), 	                                   "HR", 	"HRV", 	191),
	Country(_("Cuba"), 	                                       "CU", 	"CUB", 	192),
	Country(_("Cyprus"), 	                                   "CY", 	"CYP", 	196),
	Country(_("Czech Republic"), 	                           "CZ", 	"CZE", 	203),

	Country(_("Denmark"), 	                                   "DK", 	"DNK", 	208),
	Country(_("Djibouti"), 	                                   "DJ", 	"DJI", 	262),
	Country(_("Dominica"), 	                                   "DM", 	"DMA", 	212),
	Country(_("Dominican Republic"), 	                       "DO", 	"DOM", 	214),

	Country(_("Ecuador"), 	                                   "EC", 	"ECU", 	218),
	Country(_("Egypt"), 	                                   "EG", 	"EGY", 	818),
	Country(_("El Salvador"), 	                               "SV", 	"SLV", 	222),
	Country(_("Equatorial Guinea"), 	                       "GQ", 	"GNQ", 	226),
	Country(_("Eritrea"), 	                                   "ER", 	"ERI", 	232),
	Country(_("Estonia"), 	                                   "EE", 	"EST", 	233),
	Country(_("Ethiopia"), 	                                   "ET", 	"ETH", 	231),

	Country(_("Falkland Islands (Malvinas)"), 	               "FK", 	"FLK", 	238),
	Country(_("Faroe Islands"), 	                           "FO", 	"FRO", 	234),
	Country(_("Fiji"), 	                                       "FJ", 	"FJI", 	242),
	Country(_("Finland"), 	                                   "FI", 	"FIN", 	246),
	Country(_("France"), 	                                   "FR", 	"FRA", 	250),
	Country(_("French Guiana"), 	                           "GF", 	"GUF", 	254),
	Country(_("French Polynesia"), 	                           "PF", 	"PYF", 	258),
	Country(_("French Southern Territories"), 	               "TF", 	"ATF", 	260),

	Country(_("Gabon"),                         	           "GA", 	"GAB", 	266),
	Country(_("Gambia"),                                       "GM", 	"GMB", 	270),
	Country(_("Georgia"),                                      "GE", 	"GEO", 	268),
	Country(_("Germany"),                                      "DE", 	"DEU", 	276),
	Country(_("Ghana"),                         	           "GH", 	"GHA", 	288),
	Country(_("Gibraltar"),                                    "GI", 	"GIB", 	292),
	Country(_("Greece"),                                       "GR", 	"GRC", 	300),
	Country(_("Greenland"),                                    "GL", 	"GRL", 	304),
	Country(_("Grenada"),                                      "GD", 	"GRD", 	308),
	Country(_("Guadeloupe"),                                   "GP", 	"GLP", 	312),
	Country(_("Guam"),                         	               "GU", 	"GUM", 	316),
	Country(_("Guatemala"),                                    "GT", 	"GTM", 	320),
	Country(_("Guernsey"),                                     "GG", 	"GGY", 	831),
	Country(_("Guinea"),                                       "GN", 	"GIN", 	324),
	Country(_("Guinea-Bissau"),                                "GW", 	"GNB", 	624),
	Country(_("Guyana"),                                       "GY", 	"GUY", 	328),

	Country(_("Haiti"), 	                                   "HT", 	"HTI", 	332),
	Country(_("Heard and Mcdonald Islands"), 	               "HM", 	"HMD", 	334),
	Country(_("Holy See (Vatican City State)"), 	           "VA", 	"VAT", 	336),
	Country(_("Honduras"), 	                                   "HN", 	"HND", 	340),
	Country(_("Hungary"), 	                                   "HU", 	"HUN", 	348),

	Country(_("Iceland"), 	                                   "IS", 	"ISL", 	352),
	Country(_("India"), 	                                   "IN", 	"IND", 	356),
	Country(_("Indonesia"), 	                               "ID", 	"IDN", 	360),
	Country(_("Iran, Islamic Republic of"), 	               "IR", 	"IRN", 	364),
	Country(_("Iraq"), 	                                       "IQ", 	"IRQ", 	368),
	Country(_("Ireland"), 	                                   "IE", 	"IRL", 	372),
	Country(_("Isle of Man"), 	                               "IM", 	"IMN", 	833),
	Country(_("Israel"), 	                                   "IL", 	"ISR", 	376),
	Country(_("Italy"), 	                                   "IT", 	"ITA", 	380),

	Country(_("Jamaica"), 	                                   "JM", 	"JAM", 	388),
	Country(_("Japan"), 	                                   "JP", 	"JPN", 	392),
	Country(_("Jersey"), 	                                   "JE", 	"JEY", 	832),
	Country(_("Jordan"), 	                                   "JO", 	"JOR", 	400),

	Country(_("Kazakhstan"), 	                               "KZ", 	"KAZ", 	398),
	Country(_("Kenya"), 	                                   "KE", 	"KEN", 	404),
	Country(_("Kiribati"), 	                                   "KI", 	"KIR", 	296),
	Country(_("Korea (North)"), 	                           "KP", 	"PRK", 	408),
	Country(_("Korea (South)"), 	                           "KR", 	"KOR", 	410),
	Country(_("Kuwait"), 	                                   "KW", 	"KWT", 	414),
	Country(_("Kyrgyzstan"), 	                               "KG", 	"KGZ", 	417),

	Country(_("Lao PDR"), 	                                   "LA", 	"LAO", 	418),
	Country(_("Latvia"), 	                                   "LV", 	"LVA", 	428),
	Country(_("Lebanon"), 	                                   "LB", 	"LBN", 	422),
	Country(_("Lesotho"), 	                                   "LS", 	"LSO", 	426),
	Country(_("Liberia"), 	                                   "LR", 	"LBR", 	430),
	Country(_("Libya"), 	                                   "LY", 	"LBY", 	434),
	Country(_("Liechtenstein"), 	                           "LI", 	"LIE", 	438),
	Country(_("Lithuania"), 	                               "LT", 	"LTU", 	440),
	Country(_("Luxembourg"), 	                               "LU", 	"LUX", 	442),

	Country(_("Macedonia, Republic of"), 	                   "MK", 	"MKD", 	807),
	Country(_("Madagascar"), 	                               "MG", 	"MDG", 	450),
	Country(_("Malawi"), 	                                   "MW", 	"MWI", 	454),
	Country(_("Malaysia"), 	                                   "MY", 	"MYS", 	458),
	Country(_("Maldives"), 	                                   "MV", 	"MDV", 	462),
	Country(_("Mali"), 	                                       "ML", 	"MLI", 	466),
	Country(_("Malta"), 	                                   "MT", 	"MLT", 	470),
	Country(_("Marshall Islands"), 	                           "MH", 	"MHL", 	584),
	Country(_("Martinique"), 	                               "MQ", 	"MTQ", 	474),
	Country(_("Mauritania"), 	                               "MR", 	"MRT", 	478),
	Country(_("Mauritius"), 	                               "MU", 	"MUS", 	480),
	Country(_("Mayotte"), 	                                   "YT", 	"MYT", 	175),
	Country(_("Mexico"), 	                                   "MX", 	"MEX", 	484),
	Country(_("Micronesia, Federated States of"),              "FM", 	"FSM", 	583),
	Country(_("Moldova"), 	                                   "MD", 	"MDA", 	498),
	Country(_("Monaco"), 	                                   "MC", 	"MCO", 	492),
	Country(_("Mongolia"), 	                                   "MN", 	"MNG", 	496),
	Country(_("Montenegro"), 	                               "ME", 	"MNE", 	499),
	Country(_("Montserrat"), 	                               "MS", 	"MSR", 	500),
	Country(_("Morocco"), 	                                   "MA", 	"MAR", 	504),
	Country(_("Mozambique"), 	                               "MZ", 	"MOZ", 	508),
	Country(_("Myanmar"), 	                                   "MM", 	"MMR", 	104),

	Country(_("Namibia"), 	                                   "NA", 	"NAM", 	516),
	Country(_("Nauru"), 	                                   "NR", 	"NRU", 	520),
	Country(_("Nepal"), 	                                   "NP", 	"NPL", 	524),
	Country(_("Netherlands"), 	                               "NL", 	"NLD", 	528),
	Country(_("Netherlands Antilles"), 	                       "AN", 	"ANT", 	530),
	Country(_("New Caledonia"), 	                           "NC", 	"NCL", 	540),
	Country(_("New Zealand"), 	                               "NZ", 	"NZL", 	554),
	Country(_("Nicaragua"), 	                               "NI", 	"NIC", 	558),
	Country(_("Niger"), 	                                   "NE", 	"NER", 	562),
	Country(_("Nigeria"), 	                                   "NG", 	"NGA", 	566),
	Country(_("Niue"), 	                                       "NU", 	"NIU", 	570),
	Country(_("Norfolk Island"), 	                           "NF", 	"NFK", 	574),
	Country(_("Northern Mariana Islands"), 	                   "MP", 	"MNP", 	580),
	Country(_("Norway"), 	                                   "NO", 	"NOR", 	578),

	Country(_("Oman"), 	                                       "OM", 	"OMN", 	512),

	Country(_("Pakistan"), 	                                   "PK", 	"PAK", 	586),
	Country(_("Palau"), 	                                   "PW", 	"PLW", 	585),
	Country(_("Palestinian Territory"), 	                   "PS", 	"PSE", 	275),
	Country(_("Panama"), 	                                   "PA", 	"PAN", 	591),
	Country(_("Papua New Guinea"), 	                           "PG", 	"PNG", 	598),
	Country(_("Paraguay"), 	                                   "PY", 	"PRY", 	600),
	Country(_("Peru"), 	                                       "PE", 	"PER", 	604),
	Country(_("Philippines"), 	                               "PH", 	"PHL", 	608),
	Country(_("Pitcairn"), 	                                   "PN", 	"PCN", 	612),
	Country(_("Poland"), 	                                   "PL", 	"POL", 	616),
	Country(_("Portugal"), 	                                   "PT", 	"PRT", 	620),
	Country(_("Puerto Rico"), 	                               "PR", 	"PRI", 	630),
	
	Country(_("Qatar"), 	                                   "QA", 	"QAT", 	634),

	Country(_("Réunion"), 	                                   "RE", 	"REU", 	638),
	Country(_("Romania"), 	                                   "RO", 	"ROU", 	642),
	Country(_("Russian Federation"), 	                       "RU", 	"RUS", 	643),
	Country(_("Rwanda"), 	                                   "RW", 	"RWA", 	646),

	Country(_("Saint-Barthélemy"), 	                           "BL", 	"BLM", 	652),
	Country(_("Saint Helena"), 	                               "SH", 	"SHN", 	654),
	Country(_("Saint Kitts and Nevis"), 	                   "KN", 	"KNA", 	659),
	Country(_("Saint Lucia"), 	                               "LC", 	"LCA", 	662),
	Country(_("Saint-Martin (French part)"), 	               "MF", 	"MAF", 	663),
	Country(_("Saint Pierre and Miquelon"), 	               "PM", 	"SPM", 	666),
	Country(_("Saint Vincent and Grenadines"), 	               "VC", 	"VCT", 	670),
	Country(_("Samoa"), 	                                   "WS", 	"WSM", 	882),
	Country(_("San Marino"), 	                               "SM", 	"SMR", 	674),
	Country(_("Sao Tome and Principe"), 	                   "ST", 	"STP", 	678),
	Country(_("Saudi Arabia"), 	                               "SA", 	"SAU", 	682),
	Country(_("Senegal"), 	                                   "SN", 	"SEN", 	686),
	Country(_("Serbia"), 	                                   "RS", 	"SRB", 	688),
	Country(_("Seychelles"), 	                               "SC", 	"SYC", 	690),
	Country(_("Sierra Leone"), 	                               "SL", 	"SLE", 	694),
	Country(_("Singapore"), 	                               "SG", 	"SGP", 	702),
	Country(_("Slovakia"), 	                                   "SK", 	"SVK", 	703),
	Country(_("Slovenia"), 	                                   "SI", 	"SVN", 	705),
	Country(_("Solomon Islands"), 	                           "SB", 	"SLB", 	 90),
	Country(_("Somalia"), 	                                   "SO", 	"SOM", 	706),
	Country(_("South Africa"), 	                               "ZA", 	"ZAF", 	710),
	Country(_("South Georgia and the South Sandwich Islands"), "GS", 	"SGS", 	239),
	Country(_("South Sudan"),                                  "SS", 	"SSD", 	728),
	Country(_("Spain"), 	                                   "ES", 	"ESP", 	724),
	Country(_("Sri Lanka"), 	                               "LK", 	"LKA", 	144),
	Country(_("Sudan"), 	                                   "SD", 	"SDN", 	736),
	Country(_("Suriname"), 	                                   "SR", 	"SUR", 	740),
	Country(_("Svalbard and Jan Mayen Islands"),               "SJ", 	"SJM", 	744),
	Country(_("Swaziland"), 	                               "SZ", 	"SWZ", 	748),
	Country(_("Sweden"), 	                                   "SE", 	"SWE", 	752),
	Country(_("Switzerland"), 	                               "CH", 	"CHE", 	756),
	Country(_("Syrian Arab Republic (Syria)"), 	               "SY", 	"SYR", 	760),

	Country(_("Taiwan, Republic of China"), 	               "TW", 	"TWN", 	158),
	Country(_("Tajikistan"), 	                               "TJ", 	"TJK", 	762),
	Country(_("Tanzania, United Republic of"), 	               "TZ", 	"TZA", 	834),
	Country(_("Thailand"), 	                                   "TH", 	"THA", 	764),
	Country(_("Timor-Leste"), 	                               "TL", 	"TLS", 	626),
	Country(_("Togo"), 	                                       "TG", 	"TGO", 	768),
	Country(_("Tokelau"), 	                                   "TK", 	"TKL", 	772),
	Country(_("Tonga"), 	                                   "TO", 	"TON", 	776),
	Country(_("Trinidad and Tobago"), 	                       "TT", 	"TTO", 	780),
	Country(_("Tunisia"), 	                                   "TN", 	"TUN", 	788),
	Country(_("Turkey"), 	                                   "TR", 	"TUR", 	792),
	Country(_("Turkmenistan"), 	                               "TM", 	"TKM", 	795),
	Country(_("Turks and Caicos Islands"), 	                   "TC", 	"TCA", 	796),
	Country(_("Tuvalu"), 	                                   "TV", 	"TUV", 	798),
	
	Country(_("Uganda"), 	                                   "UG", 	"UGA", 	800),
	Country(_("Ukraine"), 	                                   "UA", 	"UKR", 	804),
	Country(_("United Arab Emirates"), 	                       "AE", 	"ARE", 	784),
	Country(_("United Kingdom"), 	                           "GB", 	"GBR", 	826),
	Country(_("United States of America"), 	                   "US", 	"USA", 	840),
	Country(_("US Minor Outlying Islands"), 	               "UM", 	"UMI", 	581),
	Country(_("Uruguay"), 	                                   "UY", 	"URY", 	858),
	Country(_("Uzbekistan"), 	                               "UZ", 	"UZB", 	860),

	Country(_("Vanuatu"), 	                                   "VU", 	"VUT", 	548),
	Country(_("Venezuela (Bolivarian Republic)"),              "VE", 	"VEN", 	862),
	Country(_("Viet Nam"), 	                                   "VN", 	"VNM", 	704),
	Country(_("Virgin Islands, US"), 	                       "VI", 	"VIR", 	850),

	Country(_("Wallis and Futuna Islands"), 	               "WF", 	"WLF", 	876),
	Country(_("Western Sahara"), 	                           "EH", 	"ESH", 	732),

	Country(_("Yemen"), 	                                   "YE", 	"YEM", 	887),
	Country(_("Zambia"), 	                                   "ZM", 	"ZMB", 	894),
	Country(_("Zimbabwe"), 	                                   "ZW", 	"ZWE", 	716),
)