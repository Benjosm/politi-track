import { Politician } from '../lib/types';

export const mockPoliticians: Politician[] = [
  {
    id: 1,
    name: "John Doe",
    party: "Democratic",
    office: "Senate",
    term_start: new Date("2020-01-01"),
    term_end: new Date("2022-12-31")
  },
  {
    id: 2,
    name: "Jane Smith",
    party: "Republican",
    office: "House of Representatives",
    term_start: new Date("2018-01-01")
  }
];
