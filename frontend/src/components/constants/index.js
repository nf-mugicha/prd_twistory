export default {
  ERROR_MEMO: {
    link_id: -1,
    title: 'unknown',
    description: 'unknown',
    platforms: [],
    million: false,
    createAt: null
  },
  NEW_EMPTY_MEMO () {
    return {
      description: '',
      createAt: null,
      photoURL: ''
    }
  },
  PLATFORMS: ['FC', 'SFC', 'GB', '64', 'GC', 'DS', 'Wii', '3DS', 'Wii U', 'Switch']
}
