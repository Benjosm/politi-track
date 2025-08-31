import { PoliticianDetails, PoliticianSummary } from '../lib/types';

export const mockPoliticianDetails: PoliticianDetails[] = [
  {
    id: 1,
    first_name: "John",
    last_name: "Doe",
    date_of_birth: new Date("1975-04-15"),
    biography: "John Doe is a U.S. Senator representing the state of California. Prior to his political career, he was a successful civil rights attorney.",
    official_website_url: "https://www.johndoe.gov",
    source: {
      name: "OpenSecrets.org",
      url: "https://www.opensecrets.org/members-of-congress/johndoe/1",
      retrieval_date: new Date("2025-08-30")
    },
    positions: [
      {
        title: "Senator",
        jurisdiction: "California",
        start_date: new Date("2020-01-01"),
        end_date: null,
        is_current: true
      },
      {
        title: "State Representative",
        jurisdiction: "California",
        start_date: new Date("2012-01-01"),
        end_date: new Date("2019-12-31"),
        is_current: false
      }
    ],
    party_affiliations: [
      {
        party_name: "Democratic",
        start_date: new Date("2010-01-01"),
        end_date: null
      }
    ],
    committee_memberships: [
      {
        role: "Chair",
        start_date: new Date("2023-01-01"),
        end_date: null,
        committee: {
          name: "Senate Committee on Foreign Relations",
          chamber: "Senate"
        }
      }
    ],
    votes: [
      {
        vote_date: new Date("2025-07-15"),
        position: "Yes",
        bill_number: "H.R. 513",
        bill_title: "Clean Energy Transition Act"
      },
      {
        vote_date: new Date("2025-07-10"),
        position: "No",
        bill_number: "S. 202",
        bill_title: "Tax Reform and Growth Bill"
      }
    ],
    gifts_received: [
      {
        description: "Tickets to a charity gala",
        value: 500,
        report_date: new Date("2024-03-20"),
        donor: "Non-profit Organization X"
      }
    ],
    campaign_donations: [
      {
        donor_name: "Tech Solutions Inc.",
        donor_type: "Corporation",
        amount: 5000,
        date: new Date("2025-06-10")
      },
      {
        donor_name: "United Labor Union",
        donor_type: "PAC",
        amount: 2500,
        date: new Date("2025-06-05")
      }
    ],
    financial_disclosures: [
      {
        report_year: 2024,
        filing_date: new Date("2025-05-15"),
        document_url: "https://www.ethics.gov/2024_jdoe_disclosure.pdf"
      }
    ]
  },
  {
    id: 2,
    first_name: "Jane",
    last_name: "Smith",
    date_of_birth: new Date("1980-11-20"),
    biography: "Jane Smith is a U.S. Representative for Texas's 12th congressional district. Known for her strong fiscal conservatism.",
    official_website_url: "https://www.janesmith.house.gov",
    source: {
      name: "Ballotpedia",
      url: "https://ballotpedia.org/Jane_Smith",
      retrieval_date: new Date("2025-08-29")
    },
    positions: [
      {
        title: "U.S. Representative",
        jurisdiction: "Texas",
        start_date: new Date("2018-01-01"),
        end_date: null,
        is_current: true
      }
    ],
    party_affiliations: [
      {
        party_name: "Republican",
        start_date: new Date("2017-01-01"),
        end_date: null
      }
    ],
    committee_memberships: [
      {
        role: "Member",
        start_date: new Date("2019-01-01"),
        end_date: null,
        committee: {
          name: "House Committee on Appropriations",
          chamber: "House"
        }
      }
    ],
    votes: [
      {
        vote_date: new Date("2025-07-15"),
        position: "No",
        bill_number: "H.R. 513",
        bill_title: "Clean Energy Transition Act"
      }
    ],
    gifts_received: [],
    campaign_donations: [
      {
        donor_name: "National Rifle Association",
        donor_type: "PAC",
        amount: 10000,
        date: new Date("2025-05-20")
      }
    ],
    financial_disclosures: [
      {
        report_year: 2023,
        filing_date: new Date("2024-05-25"),
        document_url: "https://www.house.gov/ethics/2023_jsmith_disclosure.pdf"
      }
    ]
  }
];
