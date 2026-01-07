// API Base URL
const API_URL = '/api';

// Modals
let etudiantModal, livreModal, empruntModal;

// Init
document.addEventListener('DOMContentLoaded', () => {
    // Init Bootstrap modals
    etudiantModal = new bootstrap.Modal(document.getElementById('etudiantModal'));
    livreModal = new bootstrap.Modal(document.getElementById('livreModal'));
    empruntModal = new bootstrap.Modal(document.getElementById('empruntModal'));

    // Load initial data
    loadEtudiants();
    loadLivres();
    loadEmprunts();

    // Search handlers
    document.getElementById('searchEtudiant').addEventListener('input', (e) => {
        if (e.target.value.length >= 2) {
            searchEtudiants(e.target.value);
        } else {
            loadEtudiants();
        }
    });

    document.getElementById('searchLivre').addEventListener('input', (e) => {
        if (e.target.value.length >= 2) {
            searchLivres(e.target.value);
        } else {
            loadLivres();
        }
    });

    // Tab change handlers
    document.getElementById('stats-tab').addEventListener('shown.bs.tab', () => {
        loadStats();
    });
});

// ===== Utility Functions =====

function showAlert(message, type = 'success') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    document.getElementById('alertContainer').innerHTML = alertHtml;

    setTimeout(() => {
        const alert = document.querySelector('.alert');
        if (alert) alert.remove();
    }, 5000);
}

function formatDate(dateString) {
    if (!dateString) return '<span class="badge bg-warning">En cours</span>';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
}

async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Erreur serveur');
        }

        return data;
    } catch (error) {
        showAlert(error.message, 'danger');
        throw error;
    }
}

// ===== ÉTUDIANTS =====

async function loadEtudiants() {
    try {
        const etudiants = await apiRequest('/etudiants');
        displayEtudiants(etudiants);
    } catch (error) {
        console.error('Erreur chargement étudiants:', error);
    }
}

async function searchEtudiants(terme) {
    try {
        const etudiants = await apiRequest(`/etudiants/search?q=${encodeURIComponent(terme)}`);
        displayEtudiants(etudiants);
    } catch (error) {
        console.error('Erreur recherche étudiants:', error);
    }
}

function displayEtudiants(etudiants) {
    const tbody = document.getElementById('etudiantsTableBody');

    if (etudiants.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Aucun étudiant trouvé</td></tr>';
        return;
    }

    tbody.innerHTML = etudiants.map(e => `
        <tr class="fade-in">
            <td>${e.id}</td>
            <td><strong>${e.nom}</strong></td>
            <td>${e.prenom}</td>
            <td><a href="mailto:${e.email}">${e.email}</a></td>
            <td>
                <button class="btn btn-sm btn-warning btn-action" onclick="editEtudiant(${e.id})">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-action" onclick="deleteEtudiant(${e.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function showAddEtudiantModal() {
    document.getElementById('etudiantModalTitle').textContent = 'Ajouter un étudiant';
    document.getElementById('etudiantForm').reset();
    document.getElementById('etudiantId').value = '';
    etudiantModal.show();
}

async function editEtudiant(id) {
    try {
        const etudiant = await apiRequest(`/etudiants/${id}`);
        document.getElementById('etudiantModalTitle').textContent = 'Modifier un étudiant';
        document.getElementById('etudiantId').value = etudiant.id;
        document.getElementById('etudiantNom').value = etudiant.nom;
        document.getElementById('etudiantPrenom').value = etudiant.prenom;
        document.getElementById('etudiantEmail').value = etudiant.email;
        etudiantModal.show();
    } catch (error) {
        console.error('Erreur chargement étudiant:', error);
    }
}

async function saveEtudiant() {
    const id = document.getElementById('etudiantId').value;
    const data = {
        nom: document.getElementById('etudiantNom').value.trim(),
        prenom: document.getElementById('etudiantPrenom').value.trim(),
        email: document.getElementById('etudiantEmail').value.trim()
    };

    if (!data.nom || !data.prenom || !data.email) {
        showAlert('Tous les champs sont obligatoires', 'warning');
        return;
    }

    try {
        if (id) {
            await apiRequest(`/etudiants/${id}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showAlert('Étudiant modifié avec succès');
        } else {
            await apiRequest('/etudiants', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showAlert('Étudiant créé avec succès');
        }

        etudiantModal.hide();
        loadEtudiants();
    } catch (error) {
        console.error('Erreur sauvegarde étudiant:', error);
    }
}

async function deleteEtudiant(id) {
    if (!confirm('Confirmer la suppression de cet étudiant ?')) return;

    try {
        await apiRequest(`/etudiants/${id}`, { method: 'DELETE' });
        showAlert('Étudiant supprimé avec succès');
        loadEtudiants();
    } catch (error) {
        console.error('Erreur suppression étudiant:', error);
    }
}

// ===== LIVRES =====

async function loadLivres() {
    try {
        const livres = await apiRequest('/livres');
        displayLivres(livres);
    } catch (error) {
        console.error('Erreur chargement livres:', error);
    }
}

async function searchLivres(terme) {
    try {
        const livres = await apiRequest(`/livres/search?q=${encodeURIComponent(terme)}`);
        displayLivres(livres);
    } catch (error) {
        console.error('Erreur recherche livres:', error);
    }
}

function displayLivres(livres) {
    const tbody = document.getElementById('livresTableBody');

    if (livres.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Aucun livre trouvé</td></tr>';
        return;
    }

    tbody.innerHTML = livres.map(l => `
        <tr class="fade-in">
            <td><code>${l.isbn}</code></td>
            <td><strong>${l.titre}</strong></td>
            <td>${l.editeur || 'N/A'}</td>
            <td>${l.annee_publication || 'N/A'}</td>
            <td><span class="badge bg-success">${l.exemplaires_dispo || 0}</span></td>
            <td>
                <button class="btn btn-sm btn-warning btn-action" onclick="editLivre('${l.isbn}')">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger btn-action" onclick="deleteLivre('${l.isbn}')">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

function showAddLivreModal() {
    document.getElementById('livreModalTitle').textContent = 'Ajouter un livre';
    document.getElementById('livreForm').reset();
    document.getElementById('livreId').value = '';
    document.getElementById('livreISBN').disabled = false;
    livreModal.show();
}

async function editLivre(isbn) {
    try {
        const livre = await apiRequest(`/livres/${isbn}`);
        document.getElementById('livreModalTitle').textContent = 'Modifier un livre';
        document.getElementById('livreId').value = livre.isbn;
        document.getElementById('livreISBN').value = livre.isbn;
        document.getElementById('livreISBN').disabled = true;  // ISBN non modifiable
        document.getElementById('livreTitre').value = livre.titre;
        document.getElementById('livreAuteur').value = livre.editeur || '';
        document.getElementById('livreAnnee').value = livre.annee_publication || '';
        livreModal.show();
    } catch (error) {
        console.error('Erreur chargement livre:', error);
    }
}

async function saveLivre() {
    const id = document.getElementById('livreId').value;
    const isbn = document.getElementById('livreISBN').value.trim();
    const data = {
        isbn: isbn,
        titre: document.getElementById('livreTitre').value.trim(),
        auteur: document.getElementById('livreAuteur').value.trim(),  // L'API attend 'auteur' (éditeur)
        annee_publication: document.getElementById('livreAnnee').value || null
    };

    if (!isbn || !data.titre || !data.auteur) {
        showAlert('ISBN, titre et éditeur sont obligatoires', 'warning');
        return;
    }

    try {
        if (id) {
            // Modification
            await apiRequest(`/livres/${isbn}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showAlert('Livre modifié avec succès');
        } else {
            // Création
            await apiRequest('/livres', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showAlert('Livre créé avec succès');
        }

        livreModal.hide();
        loadLivres();
    } catch (error) {
        console.error('Erreur sauvegarde livre:', error);
    }
}

async function deleteLivre(isbn) {
    if (!confirm('Confirmer la suppression de ce livre ?')) return;

    try {
        await apiRequest(`/livres/${isbn}`, { method: 'DELETE' });
        showAlert('Livre supprimé avec succès');
        loadLivres();
    } catch (error) {
        console.error('Erreur suppression livre:', error);
    }
}

// ===== EMPRUNTS =====

async function loadEmprunts() {
    try {
        const emprunts = await apiRequest('/emprunts');
        displayEmprunts(emprunts);
    } catch (error) {
        console.error('Erreur chargement emprunts:', error);
    }
}

async function loadEmpruntsEnCours() {
    try {
        const emprunts = await apiRequest('/emprunts/en-cours');
        displayEmprunts(emprunts);
    } catch (error) {
        console.error('Erreur chargement emprunts en cours:', error);
    }
}

async function loadEmpruntsEnRetard() {
    try {
        const emprunts = await apiRequest('/emprunts/en-retard');
        displayEmprunts(emprunts);
    } catch (error) {
        console.error('Erreur chargement emprunts en retard:', error);
    }
}

function displayEmprunts(emprunts) {
    const tbody = document.getElementById('empruntsTableBody');

    if (emprunts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">Aucun emprunt trouvé</td></tr>';
        return;
    }

    tbody.innerHTML = emprunts.map(e => {
        const jours = e.jours_retard || 0;
        const amende = e.amende || 0;
        const retardBadge = jours > 0 ? `<span class="badge bg-danger">${jours}j</span>` : '-';
        const amendeBadge = amende > 0 ? `<span class="badge bg-warning">${amende.toFixed(2)}€</span>` : '-';

        return `
        <tr class="fade-in">
            <td>${e.id}</td>
            <td>${e.nom} ${e.prenom}</td>
            <td>${e.titre}</td>
            <td>${formatDate(e.date_emprunt)}</td>
            <td>${formatDate(e.date_retour)}</td>
            <td>${retardBadge}</td>
            <td>${amendeBadge}</td>
            <td>
                ${!e.date_retour ? `
                    <button class="btn btn-sm btn-success btn-action" onclick="retournerEmprunt(${e.id})">
                        <i class="bi bi-check-circle"></i>
                    </button>
                ` : ''}
                <button class="btn btn-sm btn-danger btn-action" onclick="deleteEmprunt(${e.id})">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        </tr>
        `;
    }).join('');
}

function showAddEmpruntModal() {
    document.getElementById('empruntForm').reset();
    empruntModal.show();
}

async function saveEmprunt() {
    const data = {
        etudiant_id: parseInt(document.getElementById('empruntEtudiantId').value),
        livre_id: document.getElementById('empruntLivreId').value.trim()  // ISBN (string)
    };

    if (!data.etudiant_id || !data.livre_id) {
        showAlert('Tous les champs sont obligatoires', 'warning');
        return;
    }

    try {
        await apiRequest('/emprunts', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        showAlert('Emprunt créé avec succès');
        empruntModal.hide();
        loadEmprunts();
    } catch (error) {
        console.error('Erreur création emprunt:', error);
    }
}

async function retournerEmprunt(id) {
    if (!confirm('Confirmer le retour de ce livre ?')) return;

    try {
        const result = await apiRequest(`/emprunts/${id}/retourner`, { method: 'POST' });

        let message = 'Livre retourné avec succès';
        if (result.amende > 0) {
            message += ` - Amende: ${result.amende.toFixed(2)}€ (${result.jours_retard} jours de retard)`;
        }

        showAlert(message, result.amende > 0 ? 'warning' : 'success');
        loadEmprunts();
    } catch (error) {
        console.error('Erreur retour emprunt:', error);
    }
}

async function deleteEmprunt(id) {
    if (!confirm('Confirmer la suppression de cet emprunt ?')) return;

    try {
        await apiRequest(`/emprunts/${id}`, { method: 'DELETE' });
        showAlert('Emprunt supprimé avec succès');
        loadEmprunts();
    } catch (error) {
        console.error('Erreur suppression emprunt:', error);
    }
}

// ===== STATISTIQUES =====

async function loadStats() {
    try {
        // Overview
        const overview = await apiRequest('/stats/overview');
        displayStatsOverview(overview);

        // Top étudiants
        const topEtudiants = await apiRequest('/stats/top-etudiants');
        displayTopEtudiants(topEtudiants);

        // Top livres
        const topLivres = await apiRequest('/stats/top-livres');
        displayTopLivres(topLivres);
    } catch (error) {
        console.error('Erreur chargement stats:', error);
    }
}

function displayStatsOverview(data) {
    const container = document.getElementById('statsOverview');
    container.innerHTML = `
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-icon text-primary"><i class="bi bi-people-fill"></i></div>
                <div class="stat-value">${data.totaux.etudiants}</div>
                <div class="stat-label">Étudiants</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-icon text-success"><i class="bi bi-book-fill"></i></div>
                <div class="stat-value">${data.totaux.livres}</div>
                <div class="stat-label">Livres</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-icon text-info"><i class="bi bi-arrow-left-right"></i></div>
                <div class="stat-value">${data.emprunts.en_cours}</div>
                <div class="stat-label">Emprunts en cours</div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stat-card">
                <div class="stat-icon text-warning"><i class="bi bi-check-circle-fill"></i></div>
                <div class="stat-value">${data.livres_disponibles}</div>
                <div class="stat-label">Livres disponibles</div>
            </div>
        </div>
    `;
}

function displayTopEtudiants(etudiants) {
    const tbody = document.getElementById('topEtudiantsTable');

    if (etudiants.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Aucune donnée</td></tr>';
        return;
    }

    tbody.innerHTML = etudiants.map((e, i) => `
        <tr>
            <td><strong>${i + 1}</strong></td>
            <td>${e.nom} ${e.prenom}</td>
            <td><span class="badge bg-primary">${e.nb_emprunts}</span></td>
        </tr>
    `).join('');
}

function displayTopLivres(livres) {
    const tbody = document.getElementById('topLivresTable');

    if (livres.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Aucune donnée</td></tr>';
        return;
    }

    tbody.innerHTML = livres.map((l, i) => `
        <tr>
            <td><strong>${i + 1}</strong></td>
            <td>${l.titre}</td>
            <td><span class="badge bg-success">${l.nb_emprunts}</span></td>
        </tr>
    `).join('');
}
