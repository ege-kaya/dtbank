import hashlib
import flask
import sqlalchemy
from flask import Flask, request
from flask import render_template
import db
from json2html import *
import json

login = False
admin = False
index = 'index_user.html'
homelink = "<br><a href='/'>Home</a>"
app = Flask(__name__)
engine = db.engine

@app.route('/')
def hello_world():
    if not login:
        return flask.redirect('/login')
    return render_template(index, title='Homepage')

@app.route('/login', methods=['GET'])
def viewlogin():
    return render_template('login.html', title='Log in')

@app.route('/login', methods=['POST'])
def postlogin():
    global login, admin, index
    body = request.form
    username = body["username"]
    password = body["password"]
    encoded = hashlib.sha256(password.encode('utf-8')).hexdigest()
    query = engine.execute("select * from database_managers WHERE username = \'%s\';" % username)
    if query.first() is None:
        query = engine.execute("select * from users WHERE username = \'%s\';" % username)
        if query.first() is None:
            return flask.render_template_string("Invalid credentials. <a href=\"/login\"><br>Back to login</a>")
        else:
            db_pw = engine.execute("select password from users WHERE username = \'%s\';" % username).first()[0]
            if encoded == db_pw:
                login = True
                return flask.redirect('/')
                index = 'index_user.html'
            else:
                return flask.render_template_string("Invalid credentials. <a href=\"/login\"><br>Back to login</a>")
    else:
        db_pw = engine.execute("select password from database_managers WHERE username = \'%s\';" % username).first()[0]
        if encoded == db_pw:
            login = True
            admin = True
            index = 'index_admin.html'
            return flask.redirect('/')
        else:
            return flask.render_template_string("Invalid credentials. <a href=\"/login\"><br>Back to login</a>")
@app.route('/add_user', methods=['GET'])
def viewadd():
    return render_template('adduser.html', title='Add user')

@app.route('/update_affinity', methods=['GET'])
def viewaff():
    return render_template('updateaff.html', title='Update affinity')

@app.route('/delete_drug', methods=['GET'])
def deldr():
    return render_template('deldr.html', title='Delete drug')

@app.route('/delete_protein', methods=['GET'])
def delpr():
    return render_template('delpr.html', title='Delete protein')

@app.route('/update_contributors', methods=['GET'])
def updatecontr():
    return render_template('updatecontr.html', title='Update contributors')

@app.route('/drug_interactions', methods=['GET'])
def druginter():
    return render_template('druginter.html', title='See drug interactions')

@app.route('/drugs/interacts', methods=['POST'])
def interacts_router():
    body = request.form
    drugbank_id = body["drugbank_id"]
    loc = '/drugs/%s/interacts' % drugbank_id
    return flask.redirect(loc)

@app.route('/drug_side_effects', methods=['GET'])
def drugse():
    return render_template('drugse.html', title='See drug side effects')

@app.route('/drugs/side_effects', methods=['POST'])
def se_router():
    body = request.form
    drugbank_id = body["drugbank_id"]
    loc = '/drugs/%s/side_effects' % drugbank_id
    return flask.redirect(loc)

@app.route('/drug_targets', methods=['GET'])
def drugtar():
    return render_template('drugtar.html', title='See drug targets')

@app.route('/drugs/targets', methods=['POST'])
def tar_router():
    body = request.form
    drugbank_id = body["drugbank_id"]
    loc = '/drugs/%s/targets' % drugbank_id
    return flask.redirect(loc)

@app.route('/protein_binders', methods=['GET'])
def protbinders():
    return render_template('protbind.html', title='See drug side effects')

@app.route('/proteins/binders', methods=['POST'])
def bind_router():
    body = request.form
    uniprot_id = body["uniprot_id"]
    loc = '/proteins/%s/binders' % uniprot_id
    return flask.redirect(loc)

@app.route('/side_effect_causers', methods=['GET'])
def se_causers():
    return render_template('secause.html', title='See drug side effects')

@app.route('/side_effects/causers', methods=['POST'])
def sec_router():
    body = request.form
    umls_cui = body["umls_cui"]
    loc = '/side_effects/%s/causers' % umls_cui
    return flask.redirect(loc)

@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html', title='Search drugs by description')

@app.route('/least_side_effects', methods=['GET'])
def lse():
    return render_template('lse.html', title='Find the drug with least side effects')

@app.route('/side_effects/least', methods=['POST'])
def lse_router():
    body = request.form
    uniprot_id = body["uniprot_id"]
    loc = '/proteins/%s/safest_drugs' % uniprot_id
    return flask.redirect(loc)

@app.route('/view_drug', methods=['GET'])
def vd():
    return render_template('vd.html', title='View a specific drug')

@app.route('/drugs/view', methods=['POST'])
def vd_router():
    body = request.form
    drugbank_id = body["drugbank_id"]
    loc = '/drugs/%s' % drugbank_id
    return flask.redirect(loc)

@app.route('/view_protein', methods=['GET'])
def vp():
    return render_template('vp.html', title='View a specific protein')

@app.route('/proteins/view', methods=['POST'])
def vp_router():
    body = request.form
    uniprot_id = body["uniprot_id"]
    loc = '/proteins/%s' % uniprot_id
    return flask.redirect(loc)

@app.route('/view_side_effect', methods=['GET'])
def vs():
    return render_template('vs.html', title='View a specific side effect')

@app.route('/side_effects/view', methods=['POST'])
def vs_router():
    body = request.form
    umls_cui = body["umls_cui"]
    loc = '/side_effects/%s' % umls_cui
    return flask.redirect(loc)

@app.route('/filter_by_aff', methods=['GET'])
def fba():
    return render_template('fba.html', title='Filter drugs by affinity')

@app.route('/users', methods=['POST'])
def add_user():
    body = request.form
    print(body)
    name = body["name"]
    username = body["username"]
    institution = body["institution"]
    password = hashlib.sha256(body["password"].encode('utf-8')).hexdigest()
    engine.execute("INSERT INTO Institutions (name, members, points) SELECT \'%s\', ARRAY[]::text[], 0 WHERE NOT EXISTS (SELECT 1 FROM Institutions WHERE name = \'%s\');" % (institution, institution))
    engine.execute("INSERT INTO Users (name, username, institution, password, points) SELECT \'%s\', \'%s\', \'%s\', \'%s\', 0 WHERE NOT EXISTS (SELECT 1 FROM Users WHERE username = \'%s\' AND institution = \'%s\');" % (name, username, institution, hashlib.sha256(password.encode('utf-8')).hexdigest(), username, institution))
    engine.execute("UPDATE Institutions SET members = array_append(members, \'%s\');" % username)
    return flask.redirect('/users')

@app.route('/drugs/update', methods=['POST'])
def update_affinity():
    body = request.form
    reaction_id = int(body["reaction_id"])
    new_affinity = float(body["affinity_nM"])
    engine.execute("UPDATE Binds SET affinity_Nm = %f WHERE reaction_id = %d;" % (new_affinity, reaction_id))
    return 200

@app.route('/drugs/delete', methods=['POST'])
def delete_drug():
    body = request.form
    drugbank_id = body["drugbank_id"]
    engine.execute("DELETE FROM Drugs WHERE drugbank_id = \'%s\';" % drugbank_id)
    return flask.redirect('/drugs')

@app.route('/proteins/delete', methods=['POST'])
def delete_protein():
    body = request.form
    uniprot_id = body["uniprot_id"]
    engine.execute("DELETE FROM Proteins WHERE uniprot_id = \'%s\';" % uniprot_id)
    return flask.redirect('/proteins')

@app.route('/reactions/contributors', methods=['POST'])
def update_contributors():
    body = request.form
    name = body["name"]
    username = body["username"]
    password = body["password"]
    reaction_id = int(body["reaction_id"])
    doi = engine.execute("SELECT doi FROM Binds WHERE reaction_id = %d;" % reaction_id).first()[0]
    institution = engine.execute("select institution from articles where doi = \'%s\';" % doi).first()[0]
    engine.execute(
        "INSERT INTO Users SELECT \'%s\', \'%s\', \'%s\', \'%s\', 0 WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = \'%s\' and institution = \'%s\');" % (name, username, institution, hashlib.sha256(password.encode('utf-8')).hexdigest(), username, institution) )
    engine.execute("UPDATE Articles SET authors = array_append(authors, \'%s\') where doi = \'%s\';" % (username, doi))
    engine.execute("UPDATE users SET points = points+2 where username = \'%s\' and institution = \'%s\';" % (username, institution))
    return flask.redirect('/articles')

@app.route('/drugs', methods=['GET'])
def view_drugs():
    results = engine.execute("SELECT * FROM Drugs;")
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

# Compliant with requirement 8
@app.route('/drugs/detailed', methods=['GET'])
def view_drugs_detailed():
    results = engine.execute("SELECT * FROM Drugs INNER JOIN Binds ON Drugs.drugbank_id = Binds.drugbank_id INNER JOIN Proteins ON Binds.uniprot_id = Proteins.uniprot_id INNER JOIN Causes ON Drugs.drugbank_id = Causes.drugbank_id INNER JOIN Side_Effects ON Causes.umls_cui = Side_Effects.umls_cui;")
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/proteins', methods=['GET'])
def view_proteins():
    results = engine.execute("SELECT * FROM Proteins;")
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/side_effects', methods=['GET'])
def view_side_effects():
    results = engine.execute("SELECT * FROM Side_Effects;")
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/reactions', methods=['GET'])
def view_reactions():
    results = engine.execute("SELECT * FROM Binds;")
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/articles', methods=['GET'])
def view_articles():
    results = engine.execute("SELECT * FROM Articles;")
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/users', methods=['GET'])
def view_users():
    results = engine.execute("SELECT * FROM Users;")
    dict = [{column: value for column, value in row.items()} for row in results]
    print(str(json2html.convert(json=json.dumps(dict))))
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/drugs/<string:drugbank_id>/interacts', methods=['GET'])
def view_interactions(drugbank_id):
    results = engine.execute("SELECT * FROM Interacts WHERE drugbank_id_1 = \'%s\';" % drugbank_id)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/drugs/<string:drugbank_id>/side_effects', methods=['GET'])
def get_side_effects(drugbank_id):
    results = engine.execute("SELECT * FROM Causes INNER JOIN Side_Effects ON Causes.umls_cui = Side_Effects.umls_cui WHERE drugbank_id = \'%s\';" % drugbank_id)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/drugs/<string:drugbank_id>/targets', methods=['GET'])
def view_targets(drugbank_id):
    results = engine.execute("SELECT * FROM Binds INNER JOIN Proteins ON Binds.uniprot_id = Proteins.uniprot_id WHERE drugbank_id = \'%s\';" % drugbank_id)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/proteins/<string:uniprot_id>/binders', methods=['GET'])
def view_binders(uniprot_id):
    results = engine.execute("SELECT * FROM Binds INNER JOIN Drugs ON Binds.drugbank_id = Drugs.drugbank_id WHERE uniprot_id = \'%s\';" % uniprot_id)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/side_effects/<string:umls_cui>/causers', methods=['GET'])
def view_causers(umls_cui):
    results = engine.execute("SELECT drugs.drugbank_id, drugs.name FROM Causes INNER JOIN Drugs ON Causes.drugbank_id = Drugs.drugbank_id WHERE umls_cui = \'%s\';" % umls_cui)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/drugs/search', methods=['GET'])
def search_drugs():
    keyword = request.args.get('keyword', None)
    keyword = '%' + keyword + '%'
    query_string = sqlalchemy.text("SELECT * FROM Drugs WHERE Drugs.description LIKE '%s';" % keyword)
    results = engine.execute(query_string)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/proteins/<string:uniprot_id>/safest_drugs', methods=['GET'])
def get_least_side_effects(uniprot_id):
    results = engine.execute("select drugbank_id, drug_name from (SELECT drugbank_id, drug_name, COUNT(foo.umls_cui) as no_side_effects FROM (SELECT drugs.drugbank_id, drugs.name as drug_name, drugs.description, drugs.smiles, binds.uniprot_id, binds.reaction_id, binds.doi, binds.affinity_nm, binds.measure, proteins.sequence, proteins.name as protein_name, side_effects.umls_cui, side_effects.name as side_effect_name FROM Drugs INNER JOIN Binds ON Drugs.drugbank_id = Binds.drugbank_id INNER JOIN Proteins ON Binds.uniprot_id = Proteins.uniprot_id INNER JOIN Causes ON Drugs.drugbank_id = Causes.drugbank_id INNER JOIN Side_Effects ON Causes.umls_cui = Side_Effects.umls_cui WHERE Proteins.uniprot_id = \'%s\') AS foo GROUP BY foo.drugbank_id, foo.drug_name ORDER BY no_side_effects ASC) as boz where no_side_effects =  (select no_side_effects as val from (SELECT drugbank_id, COUNT(foo.umls_cui) as no_side_effects FROM (SELECT drugs.drugbank_id, drugs.name as drug_name, drugs.description, drugs.smiles, binds.uniprot_id, binds.reaction_id, binds.doi, binds.affinity_nm, binds.measure, proteins.sequence, proteins.name as protein_name, side_effects.umls_cui, side_effects.name as side_effect_name FROM Drugs INNER JOIN Binds ON Drugs.drugbank_id = Binds.drugbank_id INNER JOIN Proteins ON Binds.uniprot_id = Proteins.uniprot_id INNER JOIN Causes ON Drugs.drugbank_id = Causes.drugbank_id INNER JOIN Side_Effects ON Causes.umls_cui = Side_Effects.umls_cui WHERE Proteins.uniprot_id = \'%s\') AS foo GROUP BY foo.drugbank_id ORDER BY no_side_effects ASC) as baz limit 1);" % (uniprot_id, uniprot_id))
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/institutions/ranked', methods=['GET'])
def get_ranked():
    results = engine.execute("SELECT * FROM Institutions ORDER BY Institutions.points DESC;")
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/drugs/<string:drugbank_id>', methods=['GET'])
def view_drug(drugbank_id):
    results = engine.execute("SELECT * FROM Drugs WHERE Drugs.drugbank_id = \'%s\';" % drugbank_id)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/proteins/<string:uniprot_id>', methods=['GET'])
def view_protein(uniprot_id):
    results = engine.execute("SELECT * FROM Proteins WHERE Proteins.uniprot_id = \'%s\';" % uniprot_id)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/side_effects/<string:umls_cui>', methods=['GET'])
def view_side_effect(umls_cui):
    results = engine.execute("SELECT * FROM Side_Effects WHERE Side_Effects.umls_cui = \'%s\';" % umls_cui)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200

@app.route('/drugs/filter', methods=['GET'])
def filter_by_aff():
    drugbank_id = request.args.get('drugbank_id', None)
    minaff = request.args.get('minaff', None)
    maxaff = request.args.get('maxaff', None)
    measure = request.args.get('measure', None)
    query_string = "SELECT uniprot_id, prot_name FROM filterbyaff(%f, %f, \'%s\') WHERE drugbank_id = \'%s\';" % (float(minaff), float(maxaff), measure, drugbank_id)
    print(query_string)
    results = engine.execute(query_string)
    dict = [{column: value for column, value in row.items()} for row in results]
    return flask.render_template_string(str(json2html.convert(json=json.dumps(dict)))+homelink), 200
if __name__ == '__main__':
    app.run()
