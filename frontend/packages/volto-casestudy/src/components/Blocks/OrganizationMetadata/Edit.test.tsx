import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/react';
import OrganizationMetadataEdit from './Edit';

vi.mock('@plone/volto/components/manage/Sidebar/SidebarPortal', () => ({
  default: ({
    selected,
    children,
  }: {
    selected: boolean;
    children: React.ReactNode;
  }) => (selected ? <div data-testid="sidebar">{children}</div> : null),
}));

vi.mock('./Data', () => ({
  default: ({ block }: { block: string }) => (
    <div data-testid="data-form" data-block={block} />
  ),
}));

vi.mock('react-intl', () => ({
  defineMessages: (messages: Record<string, unknown>) => messages,
  useIntl: () => ({
    formatMessage: ({ defaultMessage }: { defaultMessage: string }) =>
      defaultMessage,
  }),
}));

const SOURCE = [{ '@id': 'http://localhost:8080/Plone/another-organization' }];

function renderEdit(
  props: Partial<React.ComponentProps<typeof OrganizationMetadataEdit>> = {},
) {
  return render(
    <OrganizationMetadataEdit
      data={{ '@type': 'organization_metadata' }}
      block="b1"
      selected={false}
      onChangeBlock={vi.fn()}
      {...props}
    />,
  );
}

describe('OrganizationMetadataEdit', () => {
  it('names the block in the editor placeholder', () => {
    const { getByText } = renderEdit();
    expect(getByText('Organization Metadata Block')).toBeTruthy();
  });

  it('says it uses the current page when no source is picked', () => {
    const { getByText, container } = renderEdit();
    expect(getByText('Current context page properties')).toBeTruthy();
    expect(container.querySelector('code')).toBeNull();
  });

  it('shows the picked source path', () => {
    const { getByText, container } = renderEdit({
      data: { '@type': 'organization_metadata', organization_source: SOURCE },
    });
    expect(getByText(/Custom page selection/)).toBeTruthy();
    expect(container.querySelector('code')?.textContent).toBe(SOURCE[0]['@id']);
  });

  it('treats an empty source list as no selection', () => {
    const { getByText } = renderEdit({
      data: { '@type': 'organization_metadata', organization_source: [] },
    });
    expect(getByText('Current context page properties')).toBeTruthy();
  });

  it('opens the sidebar form only while the block is selected', () => {
    const { queryByTestId } = renderEdit({ selected: false });
    expect(queryByTestId('sidebar')).toBeNull();

    const selected = renderEdit({ selected: true });
    expect(selected.queryByTestId('sidebar')).toBeTruthy();
  });

  it('hands the block id to the sidebar form', () => {
    const { getByTestId } = renderEdit({ selected: true });
    expect(getByTestId('data-form').getAttribute('data-block')).toBe('b1');
  });
});
