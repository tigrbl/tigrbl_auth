import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Overview } from './components/Overview';
import { MetadataExplorer } from './components/MetadataExplorer';
import { JWKSExplorer } from './components/JWKSExplorer';
import { VerifierConfig } from './components/VerifierConfig';
import { ValidationWorkbench } from './components/ValidationWorkbench';
import { TabId } from './lib/data';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabId>('overview');

  const renderContent = () => {
    switch (activeTab) {
      case 'overview': return <Overview />;
      case 'metadata': return <MetadataExplorer />;
      case 'jwks': return <JWKSExplorer />;
      case 'config': return <VerifierConfig />;
      case 'validation': return <ValidationWorkbench />;
      default: return <Overview />;
    }
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans selection:bg-indigo-100 selection:text-indigo-900">
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="flex-1 overflow-y-auto p-8 lg:p-12">
        <div className="mx-auto max-w-6xl">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}
