#!/usr/bin/env python3
"""
Application Flask - API REST pour la gestion de bibliothèque
"""

from flask import Flask, jsonify, request, render_template
from config.database import test_connection
from models import etudiant, livre, emprunt
from services import stats_service
from utils.validators import valider_email, valider_non_vide, valider_annee
from utils.logger import log

app = Flask(__name__)


# Routes Pages HTML
@app.route('/')
def index():
    """Page principale de l'application"""
    return render_template('index.html')


# API Étudiants
@app.route('/api/etudiants', methods=['GET'])
def get_etudiants():
    """Récupère tous les étudiants"""
    try:
        etudiants = etudiant.get_all()
        return jsonify(etudiants), 200
    except Exception as e:
        log(f"Erreur GET /api/etudiants: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/etudiants/<int:etudiant_id>', methods=['GET'])
def get_etudiant(etudiant_id):
    """Récupère un étudiant par ID"""
    try:
        etud = etudiant.get_by_id(etudiant_id)
        if etud:
            return jsonify(etud), 200
        return jsonify({'error': 'Étudiant non trouvé'}), 404
    except Exception as e:
        log(f"Erreur GET /api/etudiants/{etudiant_id}: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/etudiants/search', methods=['GET'])
def search_etudiants():
    """Recherche des étudiants"""
    try:
        terme = request.args.get('q', '')
        resultats = etudiant.search(terme)
        return jsonify(resultats), 200
    except Exception as e:
        log(f"Erreur GET /api/etudiants/search: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/etudiants', methods=['POST'])
def create_etudiant():
    """Crée un nouvel étudiant"""
    try:
        data = request.json
        nom = valider_non_vide(data.get('nom', ''), 'nom')
        prenom = valider_non_vide(data.get('prenom', ''), 'prénom')
        email_input = valider_non_vide(data.get('email', ''), 'email')

        if not valider_email(email_input):
            return jsonify({'error': 'Format email invalide'}), 400

        etudiant_id = etudiant.create(nom, prenom, email_input)
        return jsonify({'id': etudiant_id, 'message': 'Étudiant créé'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log(f"Erreur POST /api/etudiants: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/etudiants/<int:etudiant_id>', methods=['PUT'])
def update_etudiant(etudiant_id):
    """Met à jour un étudiant"""
    try:
        data = request.json
        nom = valider_non_vide(data.get('nom', ''), 'nom')
        prenom = valider_non_vide(data.get('prenom', ''), 'prénom')
        email_input = valider_non_vide(data.get('email', ''), 'email')

        if not valider_email(email_input):
            return jsonify({'error': 'Format email invalide'}), 400

        etudiant.update(etudiant_id, nom, prenom, email_input)
        return jsonify({'message': 'Étudiant modifié'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log(f"Erreur PUT /api/etudiants/{etudiant_id}: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/etudiants/<int:etudiant_id>', methods=['DELETE'])
def delete_etudiant(etudiant_id):
    """Supprime un étudiant"""
    try:
        etudiant.delete(etudiant_id)
        return jsonify({'message': 'Étudiant supprimé'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log(f"Erreur DELETE /api/etudiants/{etudiant_id}: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


# API Livres
@app.route('/api/livres', methods=['GET'])
def get_livres():
    """Récupère tous les livres"""
    try:
        livres = livre.get_all()
        return jsonify(livres), 200
    except Exception as e:
        log(f"Erreur GET /api/livres: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/livres/<string:isbn>', methods=['GET'])
def get_livre(isbn):
    """Récupère un livre par ISBN"""
    try:
        liv = livre.get_by_id(isbn)
        if liv:
            return jsonify(liv), 200
        return jsonify({'error': 'Livre non trouvé'}), 404
    except Exception as e:
        log(f"Erreur GET /api/livres/{isbn}: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/livres/search', methods=['GET'])
def search_livres():
    """Recherche des livres"""
    try:
        terme = request.args.get('q', '')
        resultats = livre.search(terme)
        return jsonify(resultats), 200
    except Exception as e:
        log(f"Erreur GET /api/livres/search: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/livres', methods=['POST'])
def create_livre():
    """Crée un nouveau livre"""
    try:
        data = request.json
        titre = valider_non_vide(data.get('titre', ''), 'titre')
        editeur = valider_non_vide(data.get('auteur', ''), 'éditeur')  # Frontend envoie 'auteur'
        isbn_val = valider_non_vide(data.get('isbn', ''), 'ISBN')
        annee = None
        if data.get('annee_publication'):
            annee = valider_annee(str(data.get('annee_publication')))

        livre_isbn = livre.create(titre, editeur, isbn_val, annee)
        return jsonify({'isbn': livre_isbn, 'message': 'Livre créé'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log(f"Erreur POST /api/livres: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/livres/<string:isbn>', methods=['PUT'])
def update_livre(isbn):
    """Met à jour un livre"""
    try:
        data = request.json
        titre = valider_non_vide(data.get('titre', ''), 'titre')
        editeur = valider_non_vide(data.get('auteur', ''), 'éditeur')  # Frontend envoie 'auteur'
        annee = None
        if data.get('annee_publication'):
            annee = valider_annee(str(data.get('annee_publication')))

        livre.update(isbn, titre, editeur, annee)
        return jsonify({'message': 'Livre modifié'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log(f"Erreur PUT /api/livres/{isbn}: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/livres/<string:isbn>', methods=['DELETE'])
def delete_livre(isbn):
    """Supprime un livre"""
    try:
        livre.delete(isbn)
        return jsonify({'message': 'Livre supprimé'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log(f"Erreur DELETE /api/livres/{isbn}: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


# API Emprunts
@app.route('/api/emprunts', methods=['GET'])
def get_emprunts():
    """Récupère tous les emprunts"""
    try:
        emprunts = emprunt.get_all()
        return jsonify(emprunts), 200
    except Exception as e:
        log(f"Erreur GET /api/emprunts: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/emprunts/en-cours', methods=['GET'])
def get_emprunts_en_cours():
    """Récupère les emprunts en cours"""
    try:
        emprunts = emprunt.get_en_cours()
        # Ajouter calculs jours retard et amende
        for emp in emprunts:
            emp['jours_retard'] = emprunt.calculer_jours_retard(emp)
            emp['amende'] = emprunt.calculer_amende(emp)
        return jsonify(emprunts), 200
    except Exception as e:
        log(f"Erreur GET /api/emprunts/en-cours: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/emprunts/en-retard', methods=['GET'])
def get_emprunts_en_retard():
    """Récupère les emprunts en retard"""
    try:
        emprunts = emprunt.get_en_retard()
        # Ajouter calculs
        for emp in emprunts:
            emp['jours_retard'] = emprunt.calculer_jours_retard(emp)
            emp['amende'] = emprunt.calculer_amende(emp)
        return jsonify(emprunts), 200
    except Exception as e:
        log(f"Erreur GET /api/emprunts/en-retard: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/emprunts', methods=['POST'])
def create_emprunt():
    """Crée un nouvel emprunt"""
    try:
        data = request.json
        etudiant_id = int(data.get('etudiant_id'))
        isbn_val = data.get('livre_id')  # Frontend envoie 'livre_id' mais c'est un ISBN

        # Vérifications
        if not etudiant.exists(etudiant_id):
            return jsonify({'error': 'Étudiant non trouvé'}), 404

        if not livre.exists(isbn_val):
            return jsonify({'error': 'Livre non trouvé'}), 404

        if not livre.est_disponible(isbn_val):
            return jsonify({'error': 'Livre non disponible'}), 400

        nb_emprunts = etudiant.count_emprunts_actifs(etudiant_id)
        if nb_emprunts >= 5:
            return jsonify({'error': 'Limite de 5 emprunts atteinte'}), 400

        emprunt_id = emprunt.create(etudiant_id, isbn_val)
        return jsonify({'id': emprunt_id, 'message': 'Emprunt créé'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log(f"Erreur POST /api/emprunts: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/emprunts/<int:emprunt_id>/retourner', methods=['POST'])
def retourner_emprunt(emprunt_id):
    """Retourne un livre (marque l'emprunt comme terminé)"""
    try:
        emp = emprunt.get_by_id(emprunt_id)
        if not emp:
            return jsonify({'error': 'Emprunt non trouvé'}), 404

        if emp['date_retour']:
            return jsonify({'error': 'Livre déjà retourné'}), 400

        jours_retard = emprunt.calculer_jours_retard(emp)
        amende_calc = emprunt.calculer_amende(emp)

        emprunt.retourner(emprunt_id)

        return jsonify({
            'message': 'Livre retourné',
            'jours_retard': jours_retard,
            'amende': amende_calc
        }), 200
    except Exception as e:
        log(f"Erreur POST /api/emprunts/{emprunt_id}/retourner: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/emprunts/<int:emprunt_id>', methods=['DELETE'])
def delete_emprunt(emprunt_id):
    """Supprime un emprunt"""
    try:
        emprunt.delete(emprunt_id)
        return jsonify({'message': 'Emprunt supprimé'}), 200
    except Exception as e:
        log(f"Erreur DELETE /api/emprunts/{emprunt_id}: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


# API Statistiques
@app.route('/api/stats/overview', methods=['GET'])
def get_stats_overview():
    """Récupère vue d'ensemble des stats"""
    try:
        totaux = stats_service.get_totaux()
        stats_emp = stats_service.get_stats_emprunts()
        livres_dispo = stats_service.get_livres_disponibles()
        taux = stats_service.get_taux_emprunt()

        return jsonify({
            'totaux': totaux,
            'emprunts': stats_emp,
            'livres_disponibles': livres_dispo,
            'taux_emprunt': round(taux, 1)
        }), 200
    except Exception as e:
        log(f"Erreur GET /api/stats/overview: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats/top-etudiants', methods=['GET'])
def get_top_etudiants():
    """Top 5 étudiants"""
    try:
        top = stats_service.get_top_etudiants(5)
        return jsonify(top), 200
    except Exception as e:
        log(f"Erreur GET /api/stats/top-etudiants: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats/top-livres', methods=['GET'])
def get_top_livres():
    """Top 5 livres"""
    try:
        top = stats_service.get_top_livres(5)
        return jsonify(top), 200
    except Exception as e:
        log(f"Erreur GET /api/stats/top-livres: {e}", level="ERROR")
        return jsonify({'error': str(e)}), 500


# Gestion d'erreurs
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Route non trouvée'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur serveur'}), 500


if __name__ == '__main__':
    log("Démarrage serveur Flask")

    # Test connexion BDD
    if not test_connection():
        print("ERREUR: Impossible de se connecter à la base de données")
        print("Vérifiez votre fichier .env et que PostgreSQL est démarré")
        exit(1)

    print("Connexion BDD OK")
    print("Serveur démarré sur http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
