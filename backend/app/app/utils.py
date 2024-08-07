from api.deps import db_dependency
from models import User
import re
from fpdf import FPDF
import xlsxwriter

def get_user_by_userName(db:db_dependency,username):
    """Retrieve a user from the database by username."""
    
    user=(db.query(User)
            .filter(User.user_name==username,User.status==1).first())

    return user

def get_user_by_email(db:db_dependency,email):
    """Retrieve a user from the database by email."""
    
    user=(db.query(User)
            .filter(User.e_mail==email,User.status==1).first())

    return user

def get_user_by_phNo(db:db_dependency,phno):
    """Retrieve a user from the database by phNo."""

    user=(db.query(User)
            .filter(User.ph_no==phno,User.status==1).first())

    return user



def phoneNo_validation(phonenumber:str):
    length = 10
    length_of_phonenumber =  len(phonenumber)
    if length == length_of_phonenumber:
        return True
    return False



def vehicleNumber_validation(vehicleNumber):
    
    # regx = "^[A-Z]{2}[\s][0-9]{2}[\s][A-Z]{1,2}[\s][0-9]{4}$"

    regx="^[A-Z]{2}\s\d{2}\s[A-Z]{2}\s\d{4}$"
    
    valid=re.match(regx,vehicleNumber)

    if valid:
        return True

    return False


def getBranchReport (reportDetails,total,type):
    
    
    if type == 1:
        class PDF(FPDF):
            def header(self):
                self.set_font("helvetica","B",16)
                self.cell(0,10,"Branch wise Income",align="C")


        pdf = PDF("P","mm","A4")
        pdf.add_page()
        headers = ["Branch ID","Name","Income"]
        
        pdf.rect(20,25,177,15)

        x1 = 78
        x2 =78
        # create a vertical line
        for name in headers:
            if name == "Income":
                break
            pdf.line(x1,25,x2,40)
            
            x1 += 58.5
            x2 += 58.5

        x1 =34
        # add header data
        for name in headers:
            pdf.text(x1,34,name)
            x1+=62
        
        x1=58
        x2=58.5
        x3=60.5

        y=40

        for branchData in reportDetails:
            pdf.set_xy(20,y)
            
            for key in branchData:
                if key == "Branch ID":
                    pdf.cell(x1,10,str(branchData[key]),align="C",border=1,ln=0)
                if key =="BranchName":
                    pdf.cell(x2,10,str(branchData[key]),align="C",border=1,ln=0)
                if key=="Income":
                    pdf.cell(x3,10,str(branchData[key]),align="C",border=1,ln=0)
            y += 10
            pdf.set_xy(20,y)

        pdf.set_xy(78, y)
        pdf.cell(58.5,10,"Total",align="C",border=1)
        pdf.cell(60.5,10,str(total),align="C",border=1)

        pdf.output("BranchIncome.pdf")
    else:
        
        workbook = xlsxwriter.Workbook("BranchwiseIncome.xlsx")
        worksheet = workbook.add_worksheet("firstSheet")

        worksheet.write("A1","Branch ID")
        worksheet.write("B1","BranchName")
        worksheet.write("C1","Income")


        for index,value in enumerate(reportDetails):
            
            worksheet.write(index+1,0,value["Branch ID"] ) # index+1 = row, 0 = column
            worksheet.write(index+1,1,value["BranchName"])
            worksheet.write(index+1,2,value["Income"])
            getIndex = index
        


        row = getIndex + 2
        worksheet.write(row,1,"Total")
        worksheet.write(row,2,total)


        workbook.close()

def invoiceDetail(invoiceNew,bookedDate,type):

    if type == 1:
        class PDF(FPDF):
            def header(self):
                self.set_font("helvetica","B",18)
                self.cell(0,7,"Invoice",align="c")
                
        pdf = PDF("P","mm","A4")

        pdf.add_page()
        pdf.set_font("helvetica","B",12)
        pdf.set_xy(5,17)
        pdf.cell(30,10,"Booked Date:")
        pdf.set_font("helvetica","",12)
        pdf.cell(30,10,text=str(bookedDate))

        pdf.rect(5,30,199.5,30)

        pdf.set_font("helvetica","B",12)
        x1=33.5
        x2=33.5

        for key in invoiceNew:
            if key=="Amount":
                break
            pdf.line(x1,30,x2,60)

            x1 += 28.5
            x2 += 28.5

        pdf.set_xy(5,40)

        for key in invoiceNew:
            pdf.cell(28.5,10,text=key,align="C")

        pdf.set_font("helvetica","",11)

        pdf.set_xy(5,60)
        for key in invoiceNew:
            pdf.cell(28.5,40,text=str(invoiceNew[key]),align="C",border=1)


        pdf.set_xy(147.5,100)
    
        pdf.cell(28.5,10,"Total",border=1,align="C",ln=0)
        pdf.cell(28.5,10,text="Rs."+str(invoiceNew["Amount"]),border=1,align="C")


            
        pdf.output("Invoice.pdf")
    else:
        
        workbook = xlsxwriter.Workbook("Invoice.xlsx")
        worksheet = workbook.add_worksheet()

        merge_format_order = workbook.add_format({
                        'bold': 1,
                        'align': 'center',
                        'valign': 'vcenter',
                        'fg_color': 'yellow'})

        center= workbook.add_format({
            
            'align':'center'
        })

        bold_and_center = workbook.add_format({
            "bold":1,
            'align':'center'
        })
        bold=workbook.add_format({"bold":1})

        worksheet.merge_range("C3:I3","Invoice",merge_format_order)
        worksheet.write("C4","Booked Date",bold)
        worksheet.write("D4",bookedDate)

        row = 5
        col = 2
        for index,key in enumerate(invoiceNew):
            worksheet.write(row,col,key,bold)
            worksheet.write(row+1,col,invoiceNew[key],center)
            col+=1

        worksheet.write(7,7,"Total",bold_and_center)
        worksheet.write("I8",invoiceNew["Amount"],center)
            
        workbook.close()










