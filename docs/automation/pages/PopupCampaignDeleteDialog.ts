import { expect, type Page } from '@playwright/test';
import { BasePage } from './BasePage';
import { validCampaign } from '../data/popupCampaignTestData';

export class PopupCampaignDeleteDialog extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async expectVisible(confirmMessage: string): Promise<void> {
    await expect(this.page.getByText(confirmMessage)).toBeVisible();
    await expect(this.field(/otp|mã otp/i)).toBeVisible();
  }

  async cancel(): Promise<void> {
    await this.byButton(/^cancel$/i).click();
  }

  async confirmDelete(otp = validCampaign.otp): Promise<void> {
    await this.field(/otp|mã otp/i).fill(otp);
    await this.byButton(/^delete$/i).click();
  }

  async expectToastMessage(message: string): Promise<void> {
    await this.expectToast(message);
  }
}
