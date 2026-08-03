import { expect, type Page } from '@playwright/test';
import { BasePage } from './BasePage';
import { users } from '../data/popupCampaignTestData';

export class CmsLoginPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async loginAsPopupManager(): Promise<void> {
    if (!users.popupManager.username || !users.popupManager.password) {
      return;
    }

    await this.page.goto('/login');
    await this.field(/username|email/i).fill(users.popupManager.username);
    await this.field(/password/i).fill(users.popupManager.password);
    await this.byButton(/login|sign in/i).click();
    await expect(this.byButton(/logout|sign out/i).or(this.page.getByText(/dashboard/i))).toBeVisible();
  }
}
