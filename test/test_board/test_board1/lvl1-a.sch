EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 11
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L 7WB3306:7WB3306DTR2G U1
U 1 1 5E678220
P 3500 1800
AR Path="/5E6781CF/5E678220" Ref="U1" Part="1"
AR Path="/5E678707/5E678220" Ref="U3" Part="1"
AR Path="/5E6EC0CC/5E678220" Ref="U13" Part="1"
F 0 "U13" H 3500 2265 50 0000 C CNN
F 1 "7WB3306DTR2G" H 3500 2174 50 0000 C CNN
F 2 "TSSOP:TSSOP-8" H 3300 1950 50 0001 C CNN
F 3 "" H 3300 1950 50 0001 C CNN
F 4 "143" H 0 0 0 0001 C CNN "kipart_id"
F 5 "7WB3306" H 0 0 0 0001 C CNN "kipart_sku"
F 6 "" H 0 0 0 0001 C CNN "kipart_status"
1 3500 1800
1 0 0 -1
$EndComp
$Comp
L 7WB3306:7WB3306DTR2G U2
U 1 1 5E6783CA
P 3500 2800
AR Path="/5E6781CF/5E6783CA" Ref="U2" Part="1"
AR Path="/5E678707/5E6783CA" Ref="U4" Part="1"
AR Path="/5E6EC0CC/5E6783CA" Ref="U15" Part="1"
F 0 "U15" H 3500 3265 50 0000 C CNN
F 1 "7WB3306DTR2G" H 3500 3174 50 0000 C CNN
F 2 "TSSOP:TSSOP-8" H 3300 2950 50 0001 C CNN
F 3 "" H 3300 2950 50 0001 C CNN
F 4 "143" H 0 0 0 0001 C CNN "kipart_id"
F 5 "7WB3306" H 0 0 0 0001 C CNN "kipart_sku"
1 3500 2800
1 0 0 -1
$EndComp
Wire Wire Line
3850 1600 4250 1600
Wire Wire Line
4250 1600 4250 1550
Wire Wire Line
4250 1550 4300 1550
$Comp
L accelerometer:LIS3DH U5
U 1 1 5E67B4BC
P 1700 2400
AR Path="/5E6781CF/5E67B4BC" Ref="U5" Part="1"
AR Path="/5E678707/5E67B4BC" Ref="U6" Part="1"
AR Path="/5E6EC0CC/5E67B4BC" Ref="U7" Part="1"
F 0 "U7" H 1700 3137 60 0000 C CNN
F 1 "LIS3DH" H 1700 3031 60 0000 C CNN
F 2 "LGA:LGA-16" H 1550 2600 60 0001 C CNN
F 3 "" H 1550 2600 60 0001 C CNN
F 4 "51" H 0 0 0 0001 C CNN "kipart_id"
F 5 "LIS3DHTR" H 0 0 0 0001 C CNN "kipart_sku"
1 1700 2400
1 0 0 -1
$EndComp
$Sheet
S 6300 3900 950 750
U 5E67F299
F0 "lvl2-a" 50
F1 "lvl2-a.sch" 50
$EndSheet
$EndSCHEMATC
