// Static registry of migrations, in order. Add new migrations to the end; never edit an
// applied one.
import type { Database } from 'better-sqlite3';
import * as m001 from './001_v2_schema.js';

export interface Migration {
  version: number;
  name: string;
  up(db: Database): void;
  down(db: Database): void;
}

export const migrations: Migration[] = [m001];
