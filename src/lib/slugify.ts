export function slugify(str: string): string {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

export function courseSlug(curso: string, universidade: string): string {
  const uniShort = universidade.split(' - ')[0].trim();
  return `${slugify(curso)}--${slugify(uniShort)}`;
}
