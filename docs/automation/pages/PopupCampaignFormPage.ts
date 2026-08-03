import { expect, type Locator, type Page } from '@playwright/test';
import { BasePage } from './BasePage';
import { validCampaign } from '../data/popupCampaignTestData';

export class PopupCampaignFormPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async expectCreatePage(): Promise<void> {
    await expect(this.page.getByRole('heading', { name: /create|tạo/i }).or(this.byButton(/^create$/i))).toBeVisible();
  }

  async expectEditPage(): Promise<void> {
    await expect(this.page.getByRole('heading', { name: /edit|chỉnh sửa/i }).or(this.byButton(/^save$/i))).toBeVisible();
  }

  async fillRequiredFields(): Promise<void> {
    await this.fillCampaignName(validCampaign.name);
    await this.fillDescription(validCampaign.description);
    await this.fillPriority(validCampaign.priority);
    await this.fillStartDate(validCampaign.startDate);
    await this.fillEndDate(validCampaign.endDate);
    await this.selectDisplayContent();
    await this.fillTitle(validCampaign.title);
    await this.fillContent(validCampaign.content);
    await this.selectAllMembersAudience();
    await this.selectPosition(validCampaign.position);
    await this.selectOnlyOnceFrequency();
  }

  async fillCampaignName(value: string): Promise<void> {
    await this.fillField(/popup name|campaign name|tên chiến dịch/i, value);
  }

  async fillDescription(value: string): Promise<void> {
    await this.field(/description|mô tả/i).fill(value);
  }

  async fillPriority(value: string): Promise<void> {
    await this.fillField(/priority/i, value);
  }

  async fillStartDate(value: string): Promise<void> {
    await this.fillField(/start date|ngày bắt đầu/i, value);
  }

  async fillEndDate(value: string): Promise<void> {
    await this.fillField(/end date|ngày kết thúc/i, value);
  }

  async enableNoEndDate(): Promise<void> {
    await this.toggleOrCheckbox(/no end date/i).check();
    await expect(this.field(/end date|ngày kết thúc/i)).toBeDisabled();
  }

  async selectDisplayContent(): Promise<void> {
    await this.toggleOrCheckbox(/display content|hiển thị nội dung/i).check();
  }

  async selectNoContentDisplayed(): Promise<void> {
    await this.toggleOrCheckbox(/no content displayed|không có nội dung/i).check();
    await expect(this.field(/title|tiêu đề/i)).toBeDisabled();
    await expect(this.field(/content|nội dung/i)).toBeDisabled();
  }

  async fillTitle(value: string): Promise<void> {
    await this.fillField(/title|tiêu đề/i, value);
  }

  async fillContent(value: string): Promise<void> {
    await this.field(/content|nội dung/i).fill(value);
  }

  async selectNavigation(type: string, link: string): Promise<void> {
    await this.selectOption(/navigation type|loại điều hướng/i, type);
    await this.fillField(/navigation link|link điều hướng/i, link);
  }

  async fillNavigationLink(link: string): Promise<void> {
    await this.fillField(/navigation link|link điều hướng/i, link);
  }

  async selectAllMembersAudience(): Promise<void> {
    await this.toggleOrCheckbox(/all members|toàn bộ hội viên|toàn bộ người dùng/i).check();
  }

  async selectCustomerSegment(segment: string): Promise<void> {
    await this.toggleOrCheckbox(/^customer segment$/i).check();
    await this.selectOption(/customer segment/i, segment);
  }

  async selectImportFileAudience(): Promise<void> {
    await this.toggleOrCheckbox(/import file/i).check();
  }

  async selectPosition(position: string): Promise<void> {
    await this.toggleOrCheckbox(new RegExp(position, 'i')).check();
  }

  async clearAllPositions(): Promise<void> {
    const positions = this.page.locator('[data-testid^="position-"], input[name*="position"]');
    const count = await positions.count();
    for (let index = 0; index < count; index += 1) {
      const checkbox = positions.nth(index);
      if (await checkbox.isChecked()) {
        await checkbox.uncheck();
      }
    }
  }

  async selectOnlyOnceFrequency(): Promise<void> {
    await this.toggleOrCheckbox(/only once|1 lần duy nhất/i).check();
  }

  async selectTimesPerDayFrequency(value?: string): Promise<void> {
    await this.toggleOrCheckbox(/x times\/day|x lần\/ngày/i).check();
    if (value !== undefined) {
      await this.field(/frequency value|x times|x lần/i).fill(value);
    }
  }

  async clickCreate(): Promise<void> {
    await this.byButton(/^create$/i).click();
  }

  async clickSave(): Promise<void> {
    await this.byButton(/^save$/i).click();
  }

  async clickClose(): Promise<void> {
    await this.byButton(/^close$/i).click();
  }

  async confirmCreate(otp = validCampaign.otp): Promise<void> {
    await this.fillOtp(otp);
    await this.byButton(/^yes$|^create$/i).click();
  }

  async confirmEdit(otp = validCampaign.otp): Promise<void> {
    await this.fillOtp(otp);
    await this.byButton(/^yes$|^save$/i).click();
  }

  async cancelConfirmDialog(): Promise<void> {
    await this.byButton(/^cancel$/i).click();
  }

  async expectConfirmMessage(message: string): Promise<void> {
    await expect(this.page.getByText(message)).toBeVisible();
  }

  async expectValidationMessage(message: string): Promise<void> {
    await expect(this.page.getByText(message)).toBeVisible();
  }

  async expectToastMessage(message: string): Promise<void> {
    await this.expectToast(message);
  }

  async expectSaveDisabled(): Promise<void> {
    await expect(this.byButton(/^save$/i)).toBeDisabled();
  }

  async expectSaveEnabled(): Promise<void> {
    await expect(this.byButton(/^save$/i)).toBeEnabled();
  }

  async expectFieldDisabled(name: RegExp): Promise<void> {
    await expect(this.field(name)).toBeDisabled();
  }

  private async fillOtp(otp: string): Promise<void> {
    await this.field(/otp|mã otp/i).fill(otp);
  }

  private toggleOrCheckbox(name: RegExp): Locator {
    return this.page.getByRole('checkbox', { name }).or(this.page.getByRole('radio', { name })).or(this.page.getByLabel(name));
  }

  private async selectOption(label: RegExp, optionName: string): Promise<void> {
    const control = this.page.getByRole('combobox', { name: label }).or(this.field(label));
    await control.click();
    await this.page.getByRole('option', { name: optionName }).or(this.page.getByText(optionName, { exact: true })).click();
  }
}
