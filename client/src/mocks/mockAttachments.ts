import { Attachment } from '../lib/types';

export const mockAttachments: Attachment[] = [
  {
    id: 1,
    name: "Healthcare_White_Paper.pdf",
    url: "/docs/healthcare-white-paper.pdf",
    type: "PDF",
    size: 1542876,
    uploadDate: "2020-03-15T10:30:00Z",
    relatedTo: "Issue:1"
  },
  {
    id: 2,
    name: "Climate_Proposal_Summary.docx",
    url: "/docs/climate-proposal-summary.docx",
    type: "DOCX",
    size: 978345,
    uploadDate: "2021-07-22T14:15:00Z",
    relatedTo: "Issue:2"
  },
  {
    id: 3,
    name: "Campaign_Finance_Report.xlsx",
    url: "/docs/campaign-finance-report.xlsx",
    type: "XLSX",
    size: 452398,
    uploadDate: "2020-02-10T09:45:00Z",
    relatedTo: "Politician:1"
  }
];
