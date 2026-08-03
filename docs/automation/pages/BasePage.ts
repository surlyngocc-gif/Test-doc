import { expect, type Locator, type Page } from '@playwright/test';

export abstract class BasePage {
  protected readonly page: Page;

  protected constructor(page: Page) {
    this.page = page;
  }

  protected byTestId(testId: string): Locator {
    return this.page.getByTestId(testId);
  }

  protected byButton(name: string | RegExp): Locator {
    return this.page.getByRole('button', { name });
  }

  protected byLink(name: string | RegExp): Locator {
    return this.page.getByRole('link', { name });
  }

  protected byTextbox(name: string | RegExp): Locator {
    return this.page.getByRole('textbox', { name });
  }

  protected field(name: string | RegExp): Locator {
    return this.page.getByLabel(name).or(this.page.getByPlaceholder(name));
  }

  protected async expectToast(message: string): Promise<void> {
    await expect(
      this.byTestId('toast').or(this.page.getByRole('alert')).or(this.page.getByText(message)),
    ).toContainText(message);
  }

  protected async fillField(name: string | RegExp, value: string): Promise<void> {
    await this.field(name).fill(value);
  }
}
