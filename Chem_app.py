import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.MORPH])

server=app.server
###STORAGE###
storage_lst=[
    dcc.Store(id='reactant list',storage_type='session',data=[]),
    dcc.Store(id='Reactant Dropdowns',data=['Data Type','     ','Data Type']),
    dcc.Store(id='remove reactant',data=''),
    dcc.Store(id='product list',storage_type='session',data=[])
]
###TEXTS###
reaction_text=dcc.Markdown("""
>**REACTANTS**
>
>Here you'll add your reactant information. Our job in this part is to calculate the missing
info for you. You either know how many moles you want or how much to add, we'll calculate the other.
The Chemical Name is mainly
for you to tell which is which so if you prefer to write \"Reactant 1\" instead of
a 4-bromoaldehyde or what not (is that even real?), do so!""")

product_text=dcc.Markdown("""
>**PRODUCTS**
>
>Now it's time to add products. Using your reactants information, we'll calculate your
theoretical yield for each product. You can see the whole table in the next tab!
Remember to press SUBMIT!""")

stoich_explanation="Reactions aren't always one to one! Sometimes it takes two equivalents of a reactant to make one\
equivalent of product (or vice versa!). For example-- idk if this is the actual reaction but-- H2 + O2 => H2O would\
require two equivalents of H2, one of O2 and you'll get 2 of H2O. The default here is set to 1 but if that's not the case, be sure to change it!"

table_text=dcc.Markdown("""
>**REACTION TABLE**
>
>Congrats! Your reaction is set up! We took care of the other calculations so you dont have to :)""")

reactant_warning=dcc.Markdown("""
>WARNING: Do NOT add CATALYSTS as they literally do not matter stoichiometrically!!!
>(is that even a real word?)""",
                              style={'color':'red'})
###MISCELLANEOUS###
reactant_stoich=dbc.InputGroup(
    [dbc.InputGroupText('Stoichiometry',id='stoich_ex_r'),
     dbc.Input(id='stoich_r',placeholder='Equivalents',value=1),
     dbc.Tooltip(stoich_explanation,target='stoich_ex_r')]
)
reactant_name=dbc.InputGroup(
    [dbc.Input(
        id='reactant_name', placeholder='Reactant Name', type='text'
    )]
)

reactant_transfer=dbc.InputGroup(
    [dbc.Input(id='transfer_info',placeholder='Molecular Weight or Molarity',type='numeric'),
    dbc.DropdownMenu([dbc.DropdownMenuItem('grams/mol',n_clicks_timestamp=-1,id='trans_type_1'),
                      dbc.DropdownMenuItem('mol/L',n_clicks_timestamp=-1,id='trans_type_2')],
                     id='Data Type Menu 1')
    ])
amt_types=[dbc.DropdownMenuItem('grams (g)',id='r_amt1',n_clicks_timestamp=-1),
           dbc.DropdownMenuItem('Liters (L)',id='r_amt2',n_clicks_timestamp=-1),
           dbc.DropdownMenuItem('mol',id='r_amt3',n_clicks_timestamp=-1)]


reactant_amt=dbc.InputGroup(
    [dbc.Input(id='amt info',placeholder='Amount Added',type='numeric'),
     dbc.DropdownMenu([dbc.DropdownMenuItem(children=' ',id='no m',n_clicks_timestamp=-1,active=True),
                           dbc.DropdownMenuItem('milli-',id='yes m',n_clicks_timestamp=-1)],id='milli rocks'),
     dbc.DropdownMenu(amt_types,id='r amt type')
     ]
)

sub_reactant=html.Div([dbc.Button('Add Reactant!',n_clicks=0,color='success',
                                  n_clicks_timestamp=-1,disabled=True,id='sub_react'),
html.Div(id='Disabled R Warning')])

reactant_butts=html.Div([dbc.Row(dcc.Checklist(id='react butts',options=[],value=[])),
                        dbc.Row(dbc.Button('REMOVE REACTANTS',color='danger',
                                           id='rem_r',n_clicks_timestamp=-1,n_clicks=0))])


###PRODUCT STUFF###
product_stoich=dbc.InputGroup(
    [dbc.InputGroupText('Stoichiometry',id='stoich_ex_p'),
     dbc.Input(id='stoich_p',placeholder='Equivalents',value=1),
     dbc.Tooltip(stoich_explanation,target='stoich_ex_p')]
)
product_name=dbc.InputGroup(
    [dbc.Input(
        id='product_name', placeholder='Product Name', type='text'
    )]
)

product_transfer=dbc.InputGroup(
    [dbc.Input(id='transfer_info_p',placeholder='Molecular Weight or Molarity',type='numeric'),
    dbc.DropdownMenu([dbc.DropdownMenuItem('grams/mol',n_clicks_timestamp=-1,id='trans_type_1_p'),
                      dbc.DropdownMenuItem('mol/L',n_clicks_timestamp=-1,id='trans_type_2_p')],
                     id='Product Data Type Menu 1')])

sub_prod=html.Div([dbc.Button('Add Product!',color='success',n_clicks_timestamp=-1,disabled=True,id='sub_prod'),
html.Div(id='Disabled P Warning')])

product_butts=html.Div([dbc.Row(dcc.Checklist(id='prod butts',options=[],value=[])),
                        dbc.Row(dbc.Button('REMOVE PRODUCTS',color='danger',
                                           id='rem_p',n_clicks_timestamp=-1,n_clicks=0))])

submit_all_butt=html.Div([dbc.Button('SUBMIT!',color='primary',n_clicks_timestamp=-1,disabled=True,id='sub_all'),
html.Div(id='Disabled S Warning')])

resume_button=html.Div([
    html.Button("Download My Resume!", id="resume_button",n_clicks=0),
    dcc.Download(id="resume_download")])
###Callbacks###
@app.callback(
    Output("resume_download", "data"),
    Input("resume_button", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file(
        "Assets/Gordon Liang resume 13:30.pdf"
    )
@app.callback(Output(component_id='sub_all',component_property='disabled'),
              Output(component_id='Disabled S Warning',component_property='children'),
              Input(component_id='reactant list',component_property='data'),
              Input(component_id='product list',component_property='data'))
def enable_submission(reacts,prods):
    if not reacts:
        return (True,'Add Reactants!')
    if not prods:
        return (True,'Add Products!')
    return (False,'')

@app.callback(Output(component_id='sub_prod',component_property='disabled'),
              Output(component_id='Disabled P Warning',component_property='children'),
              Input(component_id='stoich_p',component_property='value'),
              Input(component_id='transfer_info_p',component_property='value'),
              Input(component_id='Product Data Type Menu 1',component_property='label'))
def prod_button_enabling(stoichp,transp,ty):
    if ty=='Data Type':
        return (True,'Choose a Data Type!')
    if not stoichp:
        return (True,'Enter Stoichiometry Info')
    if not transp:
        return (True,'Enter Molecular Weight or Molarity')
    return (False,'')

@app.callback(Output(component_id='Product Data Type Menu 1',component_property='label'),
              Input(component_id='trans_type_1_p',component_property='n_clicks_timestamp'),
              Input(component_id='trans_type_2_p',component_property='n_clicks_timestamp'))
def prod_type(g_c,l_c):
    if g_c>l_c:
        return 'grams/mol'
    elif l_c>g_c:
        return 'mol/L'
    return 'Data Type'

@app.callback(Output(component_id='Reactant Dropdowns',component_property='data')
    ,[
    Input(component_id='trans_type_1',component_property='n_clicks_timestamp'),
    Input(component_id='trans_type_2',component_property='n_clicks_timestamp'),
    Input(component_id='no m',component_property='n_clicks_timestamp'),
    Input(component_id='yes m',component_property='n_clicks_timestamp'),
    Input(component_id='r_amt1',component_property='n_clicks_timestamp'),
    Input(component_id='r_amt2',component_property='n_clicks_timestamp'),
    Input(component_id='r_amt3',component_property='n_clicks_timestamp'),
    Input(component_id='Reactant Dropdowns',component_property='data')
])
def transtype(g_click,m_click,nom_click,mt_click,amt1,amt2,amt3,lst):
    if g_click>m_click:
        lst[0]='grams/mol'
    elif m_click>g_click:
        lst[0]='mol/L'
    else:
        lst[0]='Data Type'
    if nom_click<mt_click:
        lst[1]='milli-'
    else:
        lst[1]='      '
    if amt1==amt2==amt3:
        lst[2]='Data Type'
    else:
        tdict = {amt1: 'grams (g)',
                amt2: 'Liters (L)',
                amt3: 'mol'}
        lst[2] = tdict[max([amt1, amt2, amt3])]
    return lst

@app.callback(Output(component_id='Data Type Menu 1',component_property='label'),
              Output(component_id='milli rocks',component_property='label'),
              Output(component_id='r amt type',component_property='label'),
              Input(component_id='Reactant Dropdowns',component_property='data'))
def label_update(lst):
    return (lst[0],lst[1],lst[2])

@app.callback(Output(component_id='reactant list',component_property='data'),
              Input(component_id='sub_react',component_property='n_clicks_timestamp'), #initiates callback
              Input(component_id='rem_r',component_property='n_clicks_timestamp'), #Initiates Callback
              State(component_id='stoich_r',component_property='value'),
              State(component_id='react butts',component_property='value'),
              State(component_id='reactant_name',component_property='value'),
              State(component_id='transfer_info',component_property='value'), #mol weight/molarity
              State(component_id='Reactant Dropdowns',component_property='data'), #info types (trans/amt)
              State(component_id='amt info',component_property='value'),
              State(component_id='reactant list',component_property='data'))
def add_react(add_click,rem_click,stoichiometry,rem_val,name,transfer_info,info_lst,amt_added,lst):
    #print(lst)
    if rem_click>add_click:
        return [i for i in lst if not (i['name'] in rem_val)]
    if add_click>rem_click:
        #print(lst)
        transfer_info=float(transfer_info)
        amt_added=float(amt_added)
        trans_type,mill,amt_type=tuple(info_lst)
        if mill != 'milli-':
            amt_added = amt_added * 1000
        if amt_type=='mol':
            mmol = amt_added
            if trans_type=='grams/mol':
                    amt_added=amt_added*transfer_info
                    amt_type='mg'
            elif trans_type== 'mol/L':
                amt_added=amt_added/transfer_info
                amt_type='mL'
        elif amt_type== 'grams (g)':
            mmol=amt_added/transfer_info
            amt_type='mg'
        elif amt_type=='Liters (L)':
            mmol=amt_added*transfer_info
            amt_type='mL'
        new_lst=lst+[{'name':name,
            'stoich':float(stoichiometry),
            'Amount Added':amt_added,
            'Unit':amt_type,
            'mmol':mmol,
            'chem type': trans_type,
            'trans':transfer_info}]
        print(new_lst)
        return new_lst
    return lst


@app.callback(Output(component_id='sub_react',component_property='disabled'),
              Output(component_id='Disabled R Warning',component_property='children'),
              Input(component_id='stoich_r',component_property='value'),
              Input(component_id='reactant_name',component_property='value'),
              Input(component_id='transfer_info',component_property='value'),
              Input(component_id='amt info',component_property='value'),
              State(component_id='reactant list',component_property='data'),
              Input(component_id='Reactant Dropdowns',component_property='data'))
def enable_react(stoichr,reactant_name,trans_info,amt_info,r_lst,lst):
    if 'Data Type' in lst:
        return (True,'Pick Data Types!')
    if (lst[0]=='grams/mol' and lst[2]=='Liters (L)') or (lst[0]=='mol/L' and lst[2]=='grams (g)'):
        return (True,'Data Types are incompatible!')
    if not stoichr:
        return (True,'Enter Stoichiometry Info')
    if not trans_info:
        return (True,'Enter Molecular Weight or Molarity')
    if not amt_info:
        return (True,'Enter Amount Added')
    if not reactant_name:
        return (True,'Enter Reactant Name')
    if reactant_name in [i['name'] for i in r_lst]:
        return (True,'Reactant Name already used!')
    return (False,'')

@app.callback(Output(component_id='react butts',component_property='options'),
              Output(component_id='rem_r',component_property='disabled'),
              Input(component_id='reactant list',component_property='data'))
def update_button(list_of_reactants):
    dis=True
    if list_of_reactants:
        dis=False
    return ([{'label':i['name'],'value':i['name']} for i in list_of_reactants],dis)

@app.callback(Output(component_id='transfer_info',component_property='value'),
              Output(component_id='amt info',component_property='value'),
              Output(component_id='reactant_name',component_property='value'),
              Input(component_id='sub_react',component_property='n_clicks_timestamp'))
def reset_ins(clcks):
    return ('','','')

@app.callback(Output(component_id='transfer_info_p',component_property='value'),
              Output(component_id='product_name',component_property='value'),
              Input(component_id='sub_prod',component_property='n_clicks_timestamp'))
def reset_pins(clcks):
    return ('','')

@app.callback(Output(component_id='product list',component_property='data'),
              Input(component_id='sub_prod',component_property='n_clicks_timestamp'),
              Input(component_id='rem_p',component_property='n_clicks_timestamp'),
              State(component_id='prod butts',component_property='value'),
              State(component_id='product_name',component_property='value'),
              State(component_id='stoich_p',component_property='value'),
              State(component_id='transfer_info_p',component_property='value'),
              State(component_id='Product Data Type Menu 1',component_property='label'),
              State(component_id='product list',component_property='data'))
def add_product(add_click,rem_click,rem_val,name,stoich,trans_info,trans_type,lst):
    if rem_click>add_click:
        return [i for i in lst if not(i['name'] in rem_val)]
    if add_click>rem_click:
        return lst+[{'name':name,
                    'stoich':float(stoich),
                    'transfer info':float(trans_info),
                    'transfer type':trans_type}]
    return lst

@app.callback(Output(component_id='prod butts',component_property='options'),
              Output(component_id='rem_p',component_property='disabled'),
              Input(component_id='product list',component_property='data'))
def update_prod_button(prod_lst):
    dis=True
    if prod_lst:
        dis=False
    return ([{'label':i['name'],'value':i['name']} for i in prod_lst],dis)

@app.callback(Output(component_id='Reaction Table',component_property='disabled'),
              Output(component_id='reaction table placeholder',component_property='children'),
              Input(component_id='sub_all',component_property='n_clicks_timestamp'),
              State(component_id='reactant list',component_property='data'),
              State(component_id='product list',component_property='data'))
def df_creator(clcks,reactants,products):
    if not (reactants and products):
        return (True,[])
    total_dict={('Reactants',r['name']):{'Molecular Weight or Molarity':f'{r["trans"]} {r["chem type"]}', #FIX
                              'Amount': f'{round(r["Amount Added"],3)} {r["Unit"]}',
                              'mmol': round(r['mmol'],3)} for r in reactants}
    lim_val=min([r['mmol']/r['stoich'] for r in reactants])
    for p in products:
        mmols_created=round(lim_val*p['stoich'],3)
        if p['transfer type']=='grams/mol':
            amt=f"{mmols_created*p['transfer info']} mg"
        if p['transfer type']=='mol/L':
            amt=f"{mmols_created/p['transfer info']} mL"
        total_dict[('Products',p['name'])]={'Molecular Weight or Molarity':f'{p["transfer info"]} {p["transfer type"]}',
                                            'Amount':amt,
                                            'mmol':mmols_created}
    print(total_dict)
    df=pd.DataFrame(total_dict)
    df.index.set_names("Data Type", inplace=True)
    return (False,dbc.Table.from_dataframe(df,index=True,bordered=True,striped=True))

###LAYOUT###
chem_tablayout=dbc.Container(
    dbc.Row(
        [dbc.Col([reaction_text,
                  reactant_stoich,
                  reactant_name,
                  reactant_transfer,
                  reactant_amt,
                  sub_reactant,
                  reactant_butts,
                  reactant_warning],
                width=6),
         dbc.Col([product_text,
                  dbc.Button('Tutorial Here!',href='https://youtu.be/KkIjD-xznmE'),
                  product_stoich,
                  product_name,
                  product_transfer,
                  sub_prod,
                  product_butts,
                  submit_all_butt],width=6)]
    )
)

reaction_table=dbc.Container(
    dbc.Row(
        dbc.Col([table_text,
                 html.Div(id='reaction table placeholder')])
    )
)

Author_page=dbc.Container(
    [dbc.Row(
        dbc.Col(dcc.Markdown("""
        >**Gordon Liang**
        >
        >Hi!
        >I'm a third-year student at UC Berkeley majoring in Molecular/Cellular Biology with
        >an emphasis in Genetics and Data Science with an emphasis in Business Analytics.
        >I'm also a huge fan of baseball and my next side project will allow baseball fans
        >to see baseball from my analytical goggles! You can download my resume (please) and follow my social media below:"""))
    ),
    dbc.Row(
        dbc.Col(resume_button))
                     ]+
    [dbc.Row(
        dbc.Col(html.A(children=i[0],href=i[1]))) for i in [['Insta!','https://instagram.com/gordonliangstud?igshid=MDM4ZDc5MmU='],
                       ['YouTube!','https://www.youtube.com/channel/UCAyK1M4n3BZU34hIMhUs5_A'],
                       ['Twitter!','https://twitter.com/TalkStros']]
)
###Tabs Coming Together###
chem_tab=dbc.Tabs([
    dbc.Tab(chem_tablayout,label='Setting Up'),
    dbc.Tab(reaction_table,label='Reaction Table',disabled=True,id='Reaction Table'),
    dbc.Tab(Author_page,label='Meet Me!')
],id='tabs')


app.layout=dbc.Container(
    [dbc.Row(
        dbc.Col(html.H1('O-CHEM REACTOR TRACKER'))),
    dbc.Row(
        dbc.Col(chem_tab,width=12))
]+storage_lst,fluid=True)

if __name__ == "__main__":
    app.run_server(debug=False)
