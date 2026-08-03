import { expect, test } from '@playwright/test';
import { CmsLoginPage } from '../pages/CmsLoginPage';
import { PopupCampaignDeleteDialog } from '../pages/PopupCampaignDeleteDialog';
import { PopupCampaignFormPage } from '../pages/PopupCampaignFormPage';
import { PopupCampaignListPage } from '../pages/PopupCampaignListPage';
import {
  invalidCampaignData,
  listSearchData,
  messages,
  validCampaign,
} from '../data/popupCampaignTestData';

test.describe('CMS Pop-up campaign management', () => {
  let listPage: PopupCampaignListPage;
  let formPage: PopupCampaignFormPage;
  let deleteDialog: PopupCampaignDeleteDialog;

  test.beforeEach(async ({ page }) => {
    await new CmsLoginPage(page).loginAsPopupManager();
    listPage = new PopupCampaignListPage(page);
    formPage = new PopupCampaignFormPage(page);
    deleteDialog = new PopupCampaignDeleteDialog(page);
    await listPage.goto();
  });

  test('should display popup campaign list from menu', async () => {
    await listPage.openFromMenu();

    await expect(listPage.table).toBeVisible();
  });

  test('should search campaign by code and show No Data for unmatched keyword', async () => {
    await listPage.searchByCode(listSearchData.nonExistingCodeKeyword);

    await listPage.expectNoData();
  });

  test('should validate Search by Code max length', async () => {
    await listPage.searchByCode(listSearchData.overMaxSearchKeyword);

    await listPage.expectValidationMessage(messages.searchKeywordMaxLength);
  });

  test('should filter campaigns by Active status', async () => {
    await listPage.filterStatus('Active');

    await listPage.expectOnlyStatus('Active');
  });

  test('should not allow delete action for non-Scheduled campaigns', async () => {
    await listPage.expectDeleteUnavailableForNonScheduledCampaigns();
  });

  test('should validate required fields when creating campaign', async () => {
    await listPage.openCreateCampaign();
    await formPage.expectCreatePage();

    await formPage.clickCreate();

    await formPage.expectValidationMessage(messages.campaignNameRequired);
    await formPage.expectValidationMessage(messages.priorityRequired);
    await formPage.expectValidationMessage(messages.positionRequired);
    await formPage.expectValidationMessage(messages.frequencyRequired);
  });

  test('should validate create campaign field boundaries', async () => {
    await listPage.openCreateCampaign();
    await formPage.expectCreatePage();

    await formPage.fillCampaignName(invalidCampaignData.tooLongCampaignName);
    await formPage.fillPriority(invalidCampaignData.invalidPriority);
    await formPage.fillStartDate(invalidCampaignData.pastStartDate);
    await formPage.fillEndDate(invalidCampaignData.invalidEndDateBeforeStart);
    await formPage.clickCreate();

    await formPage.expectValidationMessage(messages.campaignNameMaxLength);
    await formPage.expectValidationMessage(messages.priorityPositiveInteger);
    await formPage.expectValidationMessage(messages.startDateNotPast);
    await formPage.expectValidationMessage(messages.endDateAfterStartDate);
  });

  test('should require navigation type when navigation link is provided', async () => {
    await listPage.openCreateCampaign();
    await formPage.expectCreatePage();
    await formPage.fillRequiredFields();
    await formPage.fillNavigationLink(validCampaign.navigationLink);

    await formPage.clickCreate();

    await formPage.expectValidationMessage(messages.navigationTypeRequired);
  });

  test('should show create confirmation for valid campaign data', async () => {
    await listPage.openCreateCampaign();
    await formPage.expectCreatePage();
    await formPage.fillRequiredFields();

    await formPage.clickCreate();

    await formPage.expectConfirmMessage(messages.createConfirm);
  });

  test('should keep user on create page when canceling unsaved changes dialog', async () => {
    await listPage.openCreateCampaign();
    await formPage.expectCreatePage();
    await formPage.fillCampaignName(validCampaign.name);

    await formPage.clickClose();
    await formPage.expectConfirmMessage(messages.unsavedChanges);
    await formPage.cancelConfirmDialog();

    await formPage.expectCreatePage();
  });

  test('should keep Save disabled when edit form has no changes', async () => {
    await listPage.openEditCampaignByStatus('Scheduled');
    await formPage.expectEditPage();

    await formPage.expectSaveDisabled();
  });

  test('should validate editable fields for Scheduled campaign', async () => {
    await listPage.openEditCampaignByStatus('Scheduled');
    await formPage.expectEditPage();

    await formPage.fillPriority(invalidCampaignData.invalidPriority);
    await formPage.clickSave();

    await formPage.expectValidationMessage(messages.priorityPositiveInteger);
  });

  test('should only enable allowed fields for Active campaign', async () => {
    await listPage.openEditCampaignByStatus('Active');
    await formPage.expectEditPage();

    await formPage.expectFieldDisabled(/priority/i);
    await formPage.expectFieldDisabled(/position/i);
  });

  test('should enable Save after valid Active campaign update', async () => {
    await listPage.openEditCampaignByStatus('Active');
    await formPage.expectEditPage();

    await formPage.fillDescription(validCampaign.updatedDescription);

    await formPage.expectSaveEnabled();
  });

  test('should validate Inactive campaign priority on edit', async () => {
    await listPage.openEditCampaignByStatus('Inactive');
    await formPage.expectEditPage();

    await formPage.fillPriority('-1');
    await formPage.clickSave();

    await formPage.expectValidationMessage(messages.priorityPositiveInteger);
  });

  test('should show edit confirmation popup for valid change', async () => {
    await listPage.openEditCampaignByStatus('Inactive');
    await formPage.expectEditPage();
    await formPage.fillDescription(validCampaign.updatedDescription);

    await formPage.clickSave();

    await formPage.expectConfirmMessage(messages.editConfirm);
  });

  test('should show delete confirmation dialog for Scheduled campaign', async () => {
    await listPage.openDeleteDialogForScheduledCampaign();

    await deleteDialog.expectVisible(messages.deleteConfirm);
  });

  test('should not delete campaign when delete confirmation is canceled', async () => {
    await listPage.openDeleteDialogForScheduledCampaign();
    await deleteDialog.expectVisible(messages.deleteConfirm);

    await deleteDialog.cancel();

    await expect(listPage.table).toBeVisible();
  });

  test('should delete Scheduled campaign successfully', async () => {
    await listPage.openDeleteDialogForScheduledCampaign();
    await deleteDialog.expectVisible(messages.deleteConfirm);

    await deleteDialog.confirmDelete();

    await deleteDialog.expectToastMessage(messages.deleteSuccess);
  });
});
