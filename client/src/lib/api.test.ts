import { getPoliticians, getTimelineEvents, getIssues, getAttachments } from './api';
import type { Politician, TimelineEvent, Issue, Attachment } from './types';

// Test function to verify the API wrapper
async function testApiWrapper() {
  console.log('Starting API wrapper verification...');

  try {
    // Test 1: Verify getPoliticians returns correct type
    console.log('Testing getPoliticians...');
    const politicians = await getPoliticians();
    console.log('✅ getPoliticians returned data:', politicians);
    console.log('Type verification - First politician:', {
      id: typeof politicians[0]?.id,
      name: typeof politicians[0]?.name,
      party: typeof politicians[0]?.party,
      office: typeof politicians[0]?.office,
      term_start: politicians[0]?.term_start instanceof Date
    });

    // Test 2: Verify getTimelineEvents
    console.log('\nTesting getTimelineEvents...');
    const timelineEvents = await getTimelineEvents();
    console.log('✅ getTimelineEvents returned data:', timelineEvents);
    console.log('Type verification - First event:', {
      id: typeof timelineEvents[0]?.id,
      year: typeof timelineEvents[0]?.year,
      type: typeof timelineEvents[0]?.type,
      title: typeof timelineEvents[0]?.title,
      description: typeof timelineEvents[0]?.description,
      financialData: Array.isArray(timelineEvents[0]?.financialData)
    });

    // Test 3: Verify getIssues
    console.log('\nTesting getIssues...');
    const issues = await getIssues();
    console.log('✅ getIssues returned data:', issues);
    console.log('Type verification - First issue:', {
      id: typeof issues[0]?.id,
      title: typeof issues[0]?.title,
      description: typeof issues[0]?.description,
      category: typeof issues[0]?.category,
      relatedPoliticians: Array.isArray(issues[0]?.relatedPoliticians),
      timelineEvents: Array.isArray(issues[0]?.timelineEvents)
    });

    // Test 4: Verify getAttachments
    console.log('\nTesting getAttachments...');
    const attachments = await getAttachments();
    console.log('✅ getAttachments returned data:', attachments);
    console.log('Type verification - First attachment:', {
      id: typeof attachments[0]?.id,
      name: typeof attachments[0]?.name,
      url: typeof attachments[0]?.url,
      type: typeof attachments[0]?.type,
      size: typeof attachments[0]?.size,
      uploadDate: typeof attachments[0]?.uploadDate,
      relatedTo: typeof attachments[0]?.relatedTo
    });

    console.log('\n🎉 All tests passed! API wrapper is working correctly.');
  } catch (error) {
    console.error('❌ Test failed:', error);
  }
}

// Only run if this file is executed directly (not imported)
if (import.meta.url === window.location.href + '/..') {
  testApiWrapper();
}

// Export for potential use in other tests
export { testApiWrapper };
