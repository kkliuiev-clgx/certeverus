# Import each of the plotting and transforma
#(consider creating a def:)

import os

import fpdf
import numpy as np
import pandas as pd

import plotly.io as pio
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

import transformation_manager as tm
import PlotSingleFactor as psf

import PlotCoverSheet as pcs
import PlotWaterfall as pwf
import singleFactorTransformation as sf
import sparklineTransformation as sl
import Waterfall_Transformation as wt
import PlotIsoquant as pi
import fhms_get_data as fm


def make_pdf(returned_chart, data, charttype): #TODO #294 User not able to makre reports due to Paramters passed and waterfall plot issues
    filePDF = "reports/"+data.replace("/"," per ")+charttype+".pdf" # sets the
    pio.write_image(returned_chart, filePDF); print('Chart Saved')  # Writes the PDF File
    

if not os.path.exists("reports"): 
    os.mkdir("reports")

# Get Data from local file/or EM -->  THIS CAN COME FROM THE FRONTEND
drivers, df, plan = fm.get_Data()

# Set Parameters for Parent, Aggregation, Grouplist, start and End Date
is_sorted = True
attributes = None
choice = None
startx = '2020-11-01'
endx = '2020-12-31'
startyear = '2020-06-01'
pva = False
parentlist = drivers['Parent'].unique()
parentlist = list(filter(lambda x: str(x) != 'nan', parentlist))
resample_period = 'MS'
ytd=False

for p in parentlist:
    if p == np.nan:
        continue

    driverlist = drivers[drivers['Parent'] == p]
    
    DriversFile, NumsFile, DenomsFile = tm.CreateDrivers(drivers, df, p, resample_period, attributes,startx,endx)
    DriversFile2, NumsFile2, DenomsFile2 = tm.CreateDrivers(drivers, df,'Free Cash Flow', resample_period,attributes,startx,endx)
    DriversFile3, NumsFile3, DenomsFile3 = tm.CreateDrivers(drivers, df, p, resample_period, attributes,startyear, endx,True)
    DriversFile.to_csv(r"./catch/FROM_TM_inReportPro56.csv")
    # print(DriversFile,driverlist)
    
    if (p != 'Free Cash Flow'):
        print('**********\n ReportPro60 RUNNING:', p, '\n***********\n')
        driverParent, targetDriver, targetNum, targetDenom, postedDrivers, postedNum, postedDenom = sf.get_SingleFactor(
            DriversFile2, NumsFile2, DenomsFile2, drivers, driver_choice=p)    
        print('completed cover 1 in ReportPro63 for:', p)
        DriversFile.to_csv(r"./catch/WTF_inReportPro64.csv")   

        x2 = wt.get_waterfall(wt.FilterSOCdates(DriversFile, endx, endx, pva=True), is_sorted, p, pva=True)
        print("X2 from ReportPro67:\n",x2)
        cover = pcs.plotCoverSheet(driverParent, targetDriver, targetNum,
                           targetDenom, postedDrivers, postedNum, postedDenom, x2)
        make_pdf(cover,p," cover")
        print('completed cover 2 in ReportPro71')
    else:
        print("skipped cover in ReportPro73 for ", p)

    DriversFile.to_csv(r"./catch/FILTERTEST_inReportPro75.csv")
    # print(startx,endx,pva,DriversFile)

    # print("WFF:\n",wt.FilterSOCdates(DriversFile, startx, endx, pva))
    # print("WFR:\n",
                # wt.get_waterfall(wt.FilterSOCdates(DriversFile, startx, endx, pva), is_sorted, p),p
            # )
    waterfall = pwf.plotWaterfall(
                wt.get_waterfall(wt.FilterSOCdates(DriversFile, startx, endx, pva), is_sorted, p),p,pva,endx
            )
    sparkline = sl.Sparkline(DriversFile)
    
    make_pdf(sparkline,p," sparkline");print("ReportPro87 Sparkline for ",p)
    make_pdf(waterfall,p," waterfall");print("ReportPro88 WaterFall for ",p)

    for d in driverlist['Driver'].unique():
        driverParent, targetDriver, targetNum, targetDenom, postedDrivers, postedNum, postedDenom = sf.get_SingleFactor(
            DriversFile, NumsFile, DenomsFile, drivers, d)
        singlefactor = psf.plotSingleFactor(
                driverParent,
                targetDriver,
                targetNum,
                targetDenom,
                postedDrivers,
                postedNum,
                postedDenom
            )
        driverParenty, targetDrivery, targetNumy, targetDenomy, postedDriversy, postedNumy, postedDenomy = sf.get_SingleFactor(DriversFile3, NumsFile3, DenomsFile3, drivers, d)
        isoquant = pi.plotisoquant(
                driverParenty, targetDrivery,targetNumy,targetDenomy, postedDriversy, postedNumy, postedDenomy,attributes,True, startyear
                )
        make_pdf(singlefactor, d," single factor")
        make_pdf(isoquant, d," isoquant")
        print('Completed Driver in ReportPro108:', d, ' for ', p)

    '''
    merger = PdfFileMerger()
    merger = merger.append(apdf)
    merger = merger.append(b)
    # Write to an output PDF document
    output = open("document-output.pdf", "wb")
    merger.write('NewPDF.pdf')
    
    def merge(source_pdf_paths, target_pdf_path):
    merger = PyPDF2.PdfFileMerger()

    # append PDF source files to merger
    for pdf_path in source_pdf_paths:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            merger.append(reader)

    # write to output file
    with open(target_pdf_path, 'wb') as g:
        merger.write(g) 
    '''

