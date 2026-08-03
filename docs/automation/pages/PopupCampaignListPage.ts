import { expect, type Locator, type Page } from '@playwright/test';
import { BasePage } from './BasePage';
import { popupCampaignRoutes } from '../data/popupCampaignTestData';

export class PopupCampaignListPage extends BasePage {
  readonly table: Locator;

  constructor(page: Page) {
    super(page);
    this.table = this.byTestId('popup-campaign-table').or(this.page.getByRole('table'));
  }

  async goto(): Promise<void> {
    await this.page.goto(popupCampaignRoutes.list);
    await expect(this.page.getByRole('heading', { name: /popup|campaign/i }).or(this.table)).toBeVisible();
  }

  async openFromMenu(): Promise<void> {
    await this.byLink(/popup.*campaign|chiến dịch marketing/i)
      .or(this.page.getByText(/popup.*campaign|chiến dịch marketing/i))
      .click();
    await expect(this.table).toBeVisible();
  }

  async searchByCode(keyword: string): Promise<void> {
    await this.field(/search by code|code/i).fill(keyword);
    await this.submitSearch();
  }

  async searchByPopupName(keyword: string): Promise<void> {
    await this.field(/search by popup|popup name|campaign/i).fill(keyword);
    await this.submitSearch();
  }

  async submitSearch(): Promise<void> {
    const searchButton = this.byButton(/search|filter|apply/i);
    if (await searchButton.isVisible()) {
      await searchButton.click();
    } else {
      await this.page.keyboard.press('Enter');
    }
  }

  async filterStatus(status: string): Promise<void> {
    await this.selectCombobox(/status/i, status);
  }

  async filterCustomerSegment(segment: string): Promise<void> {
    await this.selectCombobox(/customer segment|segment/i, segment);
  }

  async filterPosition(position: string): Promise<void> {
    await this.selectCombobox(/position/i, position);
  }

  async openCreateCampaign(): Promise<void> {
    await this.byButton(/^create$/i).click();
    await expect(this.page).toHaveURL(/create|new/i);
  }

  async openEditCampaignByStatus(status: 'Scheduled' | 'Active' | 'Inactive'): Promise<void> {
    const row = this.rowByStatus(status).first();
    await expect(row).toBeVisible();
    await row.getByRole('button', { name: /edit/i }).or(row.getByTestId('edit-campaign')).click();
  }

  async openDeleteDialogForScheduledCampaign(): Promise<void> {
    const row = this.rowByStatus('Scheduled').first();
    await expect(row).toBeVisible();
    await row.getByRole('button', { name: /delete/i }).or(row.getByTestId('delete-campaign')).click();
  }

  async expectNoData(): Promise<void> {
    await expect(this.page.getByText('No Data')).toBeVisible();
  }

  async expectValidationMessage(message: string): Promise<void> {
    await expect(this.page.getByText(message)).toBeVisible();
  }

  async expectOnlyStatus(status: string): Promise<void> {
    await expect(this.table).toContainText(status);
    const unexpectedStatuses = ['Scheduled', 'Active', 'Inactive', 'Expired'].filter((item) => item !== status);
    for (const unexpectedStatus of unexpectedStatuses) {
      await expect(this.table.getByText(unexpectedStatus, { exact: true })).toHaveCount(0);
    }
  }

  async expectDeleteUnavailableForNonScheduledCampaigns(): Promise<void> {
    for (const status of ['Active', 'Inactive', 'Expired']) {
      const rows = this.rowByStatus(status);
      const count = await rows.count();
      for (let index = 0; index < count; index += 1) {
        const deleteButton = rows.nth(index).getByRole('button', { name: /delete/i }).or(rows.nth(index).getByTestId('delete-campaign'));
        if (await deleteButton.isVisible()) {
          await expect(deleteButton).toBeDisabled();
        }
      }
    }
  }

  async expectCampaignAbsent(campaignCodeOrName: string): Promise<void> {
    await expect(this.table.getByText(campaignCodeOrName, { exact: false })).toHaveCount(0);
  }

  private rowByStatus(status: string): Locator {
    return this.table.getByRole('row').filter({ hasText: status });
  }

  private async selectCombobox(label: RegExp, optionName: string): Promise<void> {
    const combobox = this.page.getByRole('combobox', { name: label }).or(this.field(label));
    await combobox.click();
    await this.page.getByRole('option', { name: optionName }).or(this.page.getByText(optionName, { exact: true })).click();
  }
}
