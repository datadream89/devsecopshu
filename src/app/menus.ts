export interface AppMenu {
  path: string;
  text: string;
  icon?: string;
  iconTheme?: string;
  submenus?: AppMenu[];
}

export const APP_MENUS: AppMenu[] = [
  {
    path: '/welcome',
    icon: 'home',
    text: 'Data Sources',
  },
  {
    path: '/basic',
    icon: 'appstore',
    text: 'Profiling',
  },
  {
    path: '/advanced',
    icon: 'group',
    text: 'Certification',
  },
  {
    path: '/series/tree',
    icon: 'bar-chart',
    text: 'PII Classification',
  },
];
