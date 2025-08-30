interface Politician {
  id: number;
  name: string;
  party: string;
}

interface FinancialDisclosure {
  amount: number;
  category: string;
  source: string;
}

interface TimelineEvent {
  id: number;
  year: number;
  type: string;
  title: string;
  description: string;
  financialData: FinancialDisclosure[];
}
