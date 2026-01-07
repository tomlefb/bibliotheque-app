import { Routes } from '@angular/router';
import { Etudiants } from './components/etudiants/etudiants';
import { Livres } from './components/livres/livres';
import { Emprunts } from './components/emprunts/emprunts';
import { Stats } from './components/stats/stats';

export const routes: Routes = [
  { path: '', redirectTo: '/etudiants', pathMatch: 'full' },
  { path: 'etudiants', component: Etudiants },
  { path: 'livres', component: Livres },
  { path: 'emprunts', component: Emprunts },
  { path: 'stats', component: Stats },
  { path: '**', redirectTo: '/etudiants' }
];
