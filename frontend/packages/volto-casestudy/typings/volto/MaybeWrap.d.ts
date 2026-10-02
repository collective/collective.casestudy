// Stand-in for Volto's `components/manage/MaybeWrap/MaybeWrap.tsx`, used
// only by `tsconfig.typecheck.json`. Volto 19.3.0 imports
// `ComponentPropsWithoutRef` as a value, which `verbatimModuleSyntax` rejects
// (TS1484), and as a source file it cannot be skipped with `skipLibCheck`.
// The signature mirrors the original. Drop this file, and its `paths` entry,
// once Volto uses a type-only import there.
import type { ComponentPropsWithoutRef, ElementType, ReactNode } from 'react';

type MaybeWrapProps<T extends ElementType> = {
  condition: boolean;
  as: T;
} & ComponentPropsWithoutRef<ElementType extends T ? 'div' : T>;

declare function MaybeWrap<T extends ElementType = 'div'>(
  props: MaybeWrapProps<T>,
): ReactNode;

export default MaybeWrap;
