export const popupCampaignRoutes = {
  list: '/cms/popup-campaigns',
  create: '/cms/popup-campaigns/create',
};

export const users = {
  popupManager: {
    username: process.env.CMS_USERNAME ?? '',
    password: process.env.CMS_PASSWORD ?? '',
  },
};

export const listSearchData = {
  existingCodeKeyword: 'POP',
  nonExistingCodeKeyword: 'NOTFOUND-CODE',
  existingCampaignNameKeyword: 'Summer',
  overMaxSearchKeyword: 'A'.repeat(256),
};

export const validCampaign = {
  name: `Automation Popup ${Date.now()}`,
  duplicateName: 'Summer Popup',
  description: 'Created by Playwright automation',
  updatedDescription: 'Updated by Playwright automation',
  priority: '1',
  startDate: '31/12/2026 10:00',
  endDate: '31/12/2026 23:59',
  title: 'Automation title',
  content: 'Automation content',
  navigationType: 'Native App',
  navigationLink: 'lotusmiles://home',
  position: 'Home',
  segment: 'Segment A',
  frequencyValue: '1',
  otp: process.env.CMS_OTP ?? '123456',
};

export const invalidCampaignData = {
  tooLongCampaignName: 'A'.repeat(256),
  tooLongDescription: 'D'.repeat(501),
  invalidPriority: '0',
  pastStartDate: '01/01/2020 10:00',
  invalidEndDateBeforeStart: '30/12/2026 10:00',
  tooLongNavigationLink: 'https://example.com/'.concat('a'.repeat(1001)),
  tooLongTitle: 'T'.repeat(101),
  tooLongContent: 'C'.repeat(301),
  invalidFrequencyValue: '50',
};

export const messages = {
  noData: 'No Data',
  searchKeywordMaxLength: 'Search keyword must not exceed 255 characters.',
  invalidDateRange: 'Invalid date range.',
  campaignNameRequired: 'Campaign name is required.',
  campaignNameMaxLength: 'Campaign name must not exceed 255 characters.',
  descriptionMaxLength: 'Campaign name must not exceed  characters.',
  priorityRequired: 'Priority is required.',
  priorityPositiveInteger: 'Priority must be a positive integer.',
  invalidStartDateFormat: 'Invalid start date format.',
  startDateNotPast: 'Start date must be greater than or equal to current time.',
  invalidEndDateFormat: 'Invalid end date format.',
  endDateAfterStartDate: 'End date must be greater than or equal to start date.',
  invalidImageFormat: 'Invalid image format.',
  imageSizeMax: 'Image size must not exceed 2MB.',
  titleRequired: 'Title is required.',
  titleMaxLength: 'Title must not exceed 225 characters.',
  contentRequired: 'Content is required.',
  contentMaxLength: 'Description must not exceed 300 characters.',
  navigationTypeRequired: 'Navigation type is required.',
  navigationLinkRequired: 'Navigation link is required.',
  webviewNavigationTypeRequired: 'Navigation Type is required.',
  navigationLinkMaxLength: 'Link must not exceed 1000 characters.',
  audienceRequired: 'Please select audience.',
  segmentRequired: 'Please select one Customer Segment.',
  importFileRequired: 'Please upload member file.',
  positionRequired: 'Please select at least one Position.',
  frequencyRequired: 'Please select frequency type.',
  frequencyValueRequired: 'Frequency value is required.',
  frequencyValueInvalid: 'Frequency value must be an integer and less than 50.',
  weekdayRequired: 'Please select at least one day of week.',
  unsavedChanges: 'Unsaved changes will be lost. Do you want to continue?',
  createConfirm: 'Are you sure you want to create this campaign?',
  createSuccess: 'Campaign has been successfully saved.',
  createFailed: 'Failed to save campaign.',
  editConfirm: 'Are you sure you want to edit the campiagn ?',
  editSuccess: 'Campaign has been successfully edited.',
  editFailed: 'Failed to edit campaign.',
  deleteConfirm: 'Are you sure you want to delete this campaign?',
  deleteSuccess: 'Campaign has been successfully deleted.',
  deleteFailed: 'Failed to delete campaign.',
  cannotDeleteCurrentStatus: 'Campaign cannot be deleted in current status.',
};
