# Created by Reece Pieri, May 2019

# -- CHANGELOG --
# v1.0, 3/5/19  - v1.0 release.
# v1.1, 7/6/19  - Added user input validation.
#               - Added error messages to status bar, for events such as invalid IP address entry.
#               - Increased maximum number of hosts to 16384 (/18).
# v1.2, 7/6/19  - Added version number to window title.
#               - Disabled window resize.

from tkinter import *
from tkinter import ttk
from netaddr import *
import telnetlib
import ipaddress

# ===== GUI WINDOW AND FRAMES ===== #
version = "v1.2"
window = Tk()
window.title("Subnet Planner " + version)
window.geometry("880x550")
window.resizable(False, False)

ipframe = Frame(window)
ipframe.pack()
subnetlabelframe = Frame(window)
subnetlabelframe.pack()
subnetframe = Frame(window)
subnetframe.pack()
buttonframe = Frame(window)
buttonframe.pack()
resultsframe = Frame(window)
resultsframe.pack()
statusframe = Frame(window)
statusframe.pack(fill=X)

# ===== VARIABLES ===== #
subnum = StringVar()
prefix = StringVar()
subnetlist = []
hostreqlist = []
subnets = []
status = StringVar()

range30 = range(1, 3)
range29 = range(3, 7)
range28 = range(7, 15)
range27 = range(15, 31)
range26 = range(31, 63)
range25 = range(63, 127)
range24 = range(127, 255)
range23 = range(255, 511)
range22 = range(511, 1023)
range21 = range(1023, 2047)
range20 = range(2047, 4095)
range19 = range(4095, 8191)
range18 = range(8191, 16383)


# ===== FUNCTION TO CREATES SUBNET AND REQUIRED HOSTS LISTS ===== #
def create_subnets():
    # Input validation.
    try:
        ipaddress.ip_network(ipent.get())
        status.set("")
        statuslbl.configure(fg="black")
    except ValueError as v:
        statuslbl.configure(fg="red")
        status.set("Invalid IP Address. Incomplete or invalid address provided.")
        return

    if "/" in ipent.get():
        status.set("")
        statuslbl.configure(fg="black")
    else:
        statuslbl.configure(fg="red")
        status.set("Invalid IP Address. Network prefix required.")
        return

    subnetlist.clear()
    hostreqlist.clear()
    for widget in subnetframe.winfo_children():
        if widget.get().isdigit():
            hostreqlist.append(widget.get())
        elif widget.get() != "":
            if " " not in widget.get():
                status.set("")
                statuslbl.configure(fg="black")
                subnetlist.append(widget.get())
            else:
                statuslbl.configure(fg="red")
                status.set('Spaces not allowed in subnet names. Error: "' + widget.get() + '"')
                return
        else:
            if len(subnetlist) == 0:
                statuslbl.configure(fg="red")
                status.set("Enter subnet names and hosts required.")
                return
    return 1


# ===== FUNCTION TO PROCESS INFORMATION AND OUTPUT VLAN INFORMATION TO TABLE ===== #
# == Solves first subnet/vlan.
def solve_subnets():
    if create_subnets() is None:
        return
    else:
        ip = IPNetwork(ipent.get())
        subnet = subnetlist[0]
        hostreq = hostreqlist[0]
        subid = ip.network

        if int(hostreq) in range30:
            prefix.set("/30")
        if int(hostreq) in range29:
            prefix.set("/29")
        if int(hostreq) in range28:
            prefix.set("/28")
        if int(hostreq) in range27:
            prefix.set("/27")
        if int(hostreq) in range26:
            prefix.set("/26")
        if int(hostreq) in range25:
            prefix.set("/25")
        if int(hostreq) in range24:
            prefix.set("/24")
        if int(hostreq) in range23:
            prefix.set("/23")
        if int(hostreq) in range22:
            prefix.set("/22")
        if int(hostreq) in range21:
            prefix.set("/21")
        if int(hostreq) in range20:
            prefix.set("/20")
        if int(hostreq) in range19:
            prefix.set("/19")
        if int(hostreq) in range18:
            prefix.set("/18")

        submask = (IPNetwork(str(subid) + prefix.get())).netmask
        gateway = subid + 1
        hosts = (IPNetwork(str(subid) + prefix.get())).size - 2
        broadcast = (IPNetwork(str(subid) + prefix.get())).broadcast

        table.insert('', 'end', values=(subnet, hostreq, subid, prefix.get(), submask, gateway, hosts, broadcast))

        vlan_counter = 10
        x = {"vlan": "vlan " + str(vlan_counter), "name": subnet, "gateway": gateway, "submask": submask}
        subnets.append(x)
        vlan_counter += 10

        # == Solves following subnets/vlans.
        try:
            subnetcounter = 1
            hostreqcounter = 1
            for sub in subnetlist:
                subnet = subnetlist[subnetcounter]
                hostreq = hostreqlist[hostreqcounter]
                subid = broadcast + 1

                if int(hostreq) in range30:
                    prefix.set("/30")
                if int(hostreq) in range29:
                    prefix.set("/29")
                if int(hostreq) in range28:
                    prefix.set("/28")
                if int(hostreq) in range27:
                    prefix.set("/27")
                if int(hostreq) in range26:
                    prefix.set("/26")
                if int(hostreq) in range25:
                    prefix.set("/25")
                if int(hostreq) in range24:
                    prefix.set("/24")
                if int(hostreq) in range23:
                    prefix.set("/23")
                if int(hostreq) in range22:
                    prefix.set("/22")
                if int(hostreq) in range21:
                    prefix.set("/21")
                if int(hostreq) in range20:
                    prefix.set("/20")
                if int(hostreq) in range19:
                    prefix.set("/19")
                if int(hostreq) in range18:
                    prefix.set("/18")

                ip = IPNetwork(str(subid) + prefix.get())
                submask = ip.netmask
                gateway = subid + 1
                hosts = ip.size - 2
                broadcast = ip.broadcast

                table.insert('', 'end',
                             values=(subnet, hostreq, subid, prefix.get(), submask, gateway, hosts, broadcast))

                x = {"vlan": "vlan " + str(vlan_counter), "name": subnet, "gateway": gateway, "submask": submask}
                subnets.append(x)
                vlan_counter += 10

                subnetcounter += 1
                hostreqcounter += 1

        except IndexError:
            pass


# ===== FUNCTION TO PROCESS ENTERED INFORMATION ===== #
# == Clears previously entered information and calls functions to process information.
def submit_btn(event=None):
    tablelist = table.get_children()
    for item in tablelist:
        table.delete(item)
    create_subnets()
    solve_subnets()


# ===== FUNCTION TO CLEAR ENTERED INFORMATION ===== #
def clear_entries():
    ipent.delete(0, END)
    for widget in subnetframe.winfo_children():
        widget.delete(0, END)
    tablelist = table.get_children()
    for item in tablelist:
        table.delete(item)
    status.set("")
    ipent.focus_set()


# ===== FUNCTION TO SEND SUBNET INFO DIRECTLY TO A SWITCH ===== #
# == Asks for switch IP address and sends all required commands to the switch to create VLANs.
def send_to_switch():
    switch = Toplevel()
    switch.grab_set()
    switch.title("Send to Switch")
    switch.geometry("275x120")
    hostframe = Frame(switch)
    hostframe.pack()
    switchip = StringVar()
    switchpwd = StringVar()

    def send_btn(event=None):
        switchip.set(switchipent.get())
        host = switchip.get()
        password = switchpwd.get().encode('ascii')
        tn = telnetlib.Telnet(host)

        if password:
            print(password)
            tn.read_until(b"Password: ")
            tn.write(password + b"\n")
            tn.write(b"enable\n")
            tn.write(b"P@ssw0rd\n")
            tn.write(b"config t\n")

            subnetcount = 0
            for subnet in subnetlist:
                vlan_num = str(subnets[subnetcount]["vlan"])
                vlan_name = str("name " + subnets[subnetcount]["name"])
                print(vlan_num)
                print(vlan_name)
                tn.write(vlan_num.encode('ascii') + b"\n")
                tn.write(vlan_name.encode('ascii') + b"\n")
                subnetcount += 1

            subnetcount = 0
            for subnet in subnetlist:
                vlan_int = str(subnets[subnetcount]["vlan"])
                vlan_gateway = str(subnets[subnetcount]["gateway"])
                vlan_mask = str(subnets[subnetcount]["submask"])
                print(vlan_int)
                print(vlan_gateway)
                print(vlan_mask)
                tn.write(b"int " + vlan_int.encode('ascii') + b"\n")
                tn.write(b"ip address " + vlan_gateway.encode('ascii') + b" " + vlan_mask.encode('ascii') + b"\n")
                subnetcount += 1
                # tn.write(b"exit\n")

            tn.write(b"end\n")

        tn.read_until(b"end")
        tn.close()
        print("Session closed.")
        switch.grab_release()
        switch.destroy()
        status.set("VLANs sent to switch.")

    switchiplbl = Label(hostframe, text="Switch IP:")
    switchiplbl.grid(row=0, column=0, padx=10, pady=5)
    switchipent = Entry(hostframe, textvariable=switchip)
    switchipent.grid(row=0, column=1, pady=5)

    switchpwdlbl = Label(hostframe, text="Switch Password: ")
    switchpwdlbl.grid(row=1, column=0, padx=10, pady=5)
    switchpwdent = Entry(hostframe, textvariable=switchpwd)
    switchpwdent.grid(row=1, column=1, pady=5)
    switchpwdent.bind("<Return>", send_btn)

    sendbtn = Button(hostframe, width=15, text="SEND", command=send_btn)
    sendbtn.grid(columnspan=2, row=2, column=0, pady=10)

    switchipent.focus_set()

    switch.mainloop()


# ===== CREATES ENTRY AND LABEL WIDGETS ===== #
iplbl = Label(ipframe, text="Enter starting address: ")
iplbl.grid(row=0, column=0, pady=5)
ipent = Entry(ipframe, width=20)
ipent.grid(row=0, column=1, pady=5)

sublbl = Label(subnetlabelframe, text="Subnet Names").grid(row=0, column=0, padx=30)
hostlbl = Label(subnetlabelframe, text="Hosts Required").grid(row=0, column=1, padx=30)

subnet1ent = Entry(subnetframe)
subnet1ent.grid(row=1, column=0, padx=10, pady=2)
hostreq1ent = Entry(subnetframe)
hostreq1ent.grid(row=1, column=1, padx=10, pady=2)
subnet2ent = Entry(subnetframe)
subnet2ent.grid(row=2, column=0, padx=10, pady=2)
hostreq2ent = Entry(subnetframe)
hostreq2ent.grid(row=2, column=1, padx=10, pady=2)
subnet3ent = Entry(subnetframe)
subnet3ent.grid(row=3, column=0, padx=10, pady=2)
hostreq3ent = Entry(subnetframe)
hostreq3ent.grid(row=3, column=1, padx=10, pady=2)
subnet4ent = Entry(subnetframe)
subnet4ent.grid(row=4, column=0, padx=10, pady=2)
hostreq4ent = Entry(subnetframe)
hostreq4ent.grid(row=4, column=1, padx=10, pady=2)
subnet5ent = Entry(subnetframe)
subnet5ent.grid(row=5, column=0, padx=10, pady=2)
hostreq5ent = Entry(subnetframe)
hostreq5ent.grid(row=5, column=1, padx=10, pady=2)
subnet6ent = Entry(subnetframe)
subnet6ent.grid(row=6, column=0, padx=10, pady=2)
hostreq6ent = Entry(subnetframe)
hostreq6ent.grid(row=6, column=1, padx=10, pady=2)
subnet7ent = Entry(subnetframe)
subnet7ent.grid(row=7, column=0, padx=10, pady=2)
hostreq7ent = Entry(subnetframe)
hostreq7ent.grid(row=7, column=1, padx=10, pady=2)
subnet8ent = Entry(subnetframe)
subnet8ent.grid(row=8, column=0, padx=10, pady=2)
hostreq8ent = Entry(subnetframe)
hostreq8ent.grid(row=8, column=1, padx=10, pady=2)

entrylist = [subnetframe.winfo_children()]
for entry in subnetframe.winfo_children():
    entry.bind("<Return>", submit_btn)

# ===== CREATES TABLE AND TABLE HEADERS ===== #
cols = ('Subnet Name', 'Hosts Required', 'Subnet ID', 'Prefix', 'Subnet Mask', 'Gateway', 'Usable Hosts', 'Broadcast')
table = ttk.Treeview(resultsframe, columns=cols, show='headings')
table.column("Subnet Name", anchor="center")
table.column("Hosts Required", anchor="center")
table.column("Subnet ID", anchor="center")
table.column("Prefix", anchor="center")
table.column("Subnet Mask", anchor="center")
table.column("Gateway", anchor="center")
table.column("Usable Hosts", anchor="center")
table.column("Broadcast", anchor="center")

for col in cols:
    table.heading(col, text=col)
    table.column(col, minwidth=10, width=100, stretch=NO)

table.grid(row=1, column=0)

# ===== CREATES STATUS BAR WIDGETS ===== #
statuslbl = Label(statusframe, width=75, anchor=W, justify=LEFT, textvariable=status)
statuslbl.pack(side=LEFT, padx=10, pady=5)
authorlbl = Label(statusframe, width=25, text="Created by Reece Pieri. May 2019")
authorlbl.pack(side=RIGHT, padx=25, pady=7)

# ===== CREATES BUTTONS ===== #
clearbtn = Button(buttonframe, text="CLEAR", width=15, command=clear_entries)
clearbtn.pack(side="left", padx=10, pady=10)
submitbtn = Button(buttonframe, text="SUBMIT", width=15, command=submit_btn)
submitbtn.pack(side="left", padx=10, pady=10)
submitbtn.bind("<Return>", submit_btn)
switchbtn = Button(buttonframe, text="SEND TO SWITCH", width=15, command=send_to_switch)
switchbtn.pack(side="left", padx=10, pady=10)

ipent.focus_set()

mainloop()
