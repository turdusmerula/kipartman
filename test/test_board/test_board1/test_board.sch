EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 11
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 3550 1300 850 350
U 5E6781CF
F0 "lvl1-a1" 50
F1 "lvl1-a.sch" 50
$EndSheet
$Sheet
S 3600 2250 950 800
U 5E678707
F0 "lvl1-a2" 50
F1 "lvl1-a.sch" 50
$EndSheet
$Comp
L accelerometer:LIS3DH U1
U 1 1 5E67E75F
P 2050 2300
F 0 "U1" H 2050 3037 60 0000 C CNN
F 1 "LIS3DHTR" H 2050 2931 60 0000 C CNN
F 2 "LGA:LGA-16" H 1900 2500 60 0001 C CNN
F 3 "" H 1900 2500 60 0001 C CNN
F 4 "51" H 0 0 0 0001 C CNN "kipart_id"
F 5 "LIS3DHTR" H 0 0 0 0001 C CNN "kipart_sku"
1 2050 2300
1 0 0 -1
$EndComp
$Comp
L adc:AD7793 U2
U 1 1 5E67EAF2
P 2100 4000
F 0 "U2" H 2100 4767 50 0000 C CNN
F 1 "AD7793" H 2100 4676 50 0000 C CNN
F 2 "SOP65P640X120-16N" H 2100 4000 50 0001 L BNN
F 3 "None" H 2100 4000 50 0001 L BNN
F 4 "Unavailable" H 2100 4000 50 0001 L BNN "Field4"
F 5 "TSSOP-16 Analog Devices" H 2100 4000 50 0001 L BNN "Field5"
F 6 "AD7793" H 2100 4000 50 0001 L BNN "Field6"
F 7 "Triple Channel Single ADC Delta-Sigma 470sps 24-bit Serial 16-Pin TSSOP T/R" H 2100 4000 50 0001 L BNN "Field7"
F 8 "Analog Devices" H 2100 4000 50 0001 L BNN "Field8"
F 9 "131" H 0 0 0 0001 C CNN "kipart_id"
F 10 "AD7793" H 0 0 0 0001 C CNN "kipart_sku"
1 2100 4000
1 0 0 -1
$EndComp
$Sheet
S 4000 3650 800 500
U 5E6EBAF2
F0 "lvl1-b" 50
F1 "lvl1-b.sch" 50
$EndSheet
$Sheet
S 4900 1300 800 350
U 5E6EC0CC
F0 "lvl1-a3" 50
F1 "lvl1-a.sch" 50
$EndSheet
$EndSCHEMATC
