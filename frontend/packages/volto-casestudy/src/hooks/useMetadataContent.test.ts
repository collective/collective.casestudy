import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useMetadataContent } from './useMetadataContent';

interface Fake {
  '@id': string;
  title: string;
}

const CURRENT: Fake = { '@id': 'http://localhost:3000/here', title: 'Here' };
const REMOTE: Fake = {
  '@id': 'http://localhost:8080/plone/there',
  title: 'There',
};

function mockFetch(impl: (url: string) => Promise<unknown>) {
  const fetchMock = vi.fn((url: string) => impl(url));
  vi.stubGlobal('fetch', fetchMock);
  return fetchMock;
}

const ok = (body: unknown) => Promise.resolve({ ok: true, json: () => body });

describe('useMetadataContent', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('uses the current page when no target is given', async () => {
    const { result } = renderHook(() =>
      useMetadataContent<Fake>(undefined, CURRENT),
    );
    await waitFor(() => expect(result.current).toEqual(CURRENT));
  });

  it('does not fetch when no target is given', async () => {
    const fetchMock = mockFetch(() => ok(REMOTE));
    renderHook(() => useMetadataContent<Fake>(undefined, CURRENT));
    await waitFor(() => expect(fetchMock).not.toHaveBeenCalled());
  });

  it('returns null when there is neither a target nor a current page', async () => {
    const { result } = renderHook(() =>
      useMetadataContent<Fake>(undefined, undefined),
    );
    await waitFor(() => expect(result.current).toBeNull());
  });

  it('fetches the referenced item through the ++api++ traverser', async () => {
    const fetchMock = mockFetch(() => ok(REMOTE));
    const { result } = renderHook(() =>
      useMetadataContent<Fake>('http://localhost:8080/plone/there', CURRENT),
    );
    await waitFor(() => expect(result.current).toEqual(REMOTE));
    // The backend origin is stripped: the request goes to the frontend, which
    // proxies it -- so it works from a browser that cannot reach Plone.
    expect(fetchMock).toHaveBeenCalledWith(
      `${window.location.origin}/++api++/plone/there`,
      { headers: { Accept: 'application/json' } },
    );
  });

  it('keeps a path that is already relative', async () => {
    const fetchMock = mockFetch(() => ok(REMOTE));
    renderHook(() => useMetadataContent<Fake>('/plone/there', CURRENT));
    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        `${window.location.origin}/++api++/plone/there`,
        expect.anything(),
      ),
    );
  });

  it('prefers the fetched item over the current page', async () => {
    mockFetch(() => ok(REMOTE));
    const { result } = renderHook(() =>
      useMetadataContent<Fake>('http://localhost:8080/plone/there', CURRENT),
    );
    await waitFor(() => expect(result.current).toEqual(REMOTE));
    expect(result.current).not.toEqual(CURRENT);
  });

  it('stays null when the response is not ok', async () => {
    mockFetch(() => Promise.resolve({ ok: false, json: () => REMOTE }));
    const { result } = renderHook(() =>
      useMetadataContent<Fake>('http://localhost:8080/plone/there', CURRENT),
    );
    await waitFor(() => expect(result.current).toBeNull());
  });

  it('swallows a rejected request instead of throwing', async () => {
    mockFetch(() => Promise.reject(new Error('offline')));
    const { result } = renderHook(() =>
      useMetadataContent<Fake>('http://localhost:8080/plone/there', CURRENT),
    );
    await waitFor(() => expect(result.current).toBeNull());
  });

  it('refetches when the target changes', async () => {
    const fetchMock = mockFetch((url: string) =>
      ok({ '@id': url, title: url.endsWith('two') ? 'Two' : 'One' }),
    );
    const { result, rerender } = renderHook(
      ({ target }: { target: string }) =>
        useMetadataContent<Fake>(target, CURRENT),
      { initialProps: { target: 'http://localhost:8080/plone/one' } },
    );
    await waitFor(() => expect(result.current?.title).toBe('One'));

    rerender({ target: 'http://localhost:8080/plone/two' });
    await waitFor(() => expect(result.current?.title).toBe('Two'));
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('falls back to the current page when the target is cleared', async () => {
    mockFetch(() => ok(REMOTE));
    const { result, rerender } = renderHook(
      ({ target }: { target: string | undefined }) =>
        useMetadataContent<Fake>(target, CURRENT),
      {
        initialProps: {
          target: 'http://localhost:8080/plone/there' as string | undefined,
        },
      },
    );
    await waitFor(() => expect(result.current).toEqual(REMOTE));

    rerender({ target: undefined });
    await waitFor(() => expect(result.current).toEqual(CURRENT));
  });
});
