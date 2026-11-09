// Real New Brunswick town waypoints, strung together into delivery routes.
// Each route is an ordered list of [lat, lng] stops along a real highway corridor.

export const ROUTES = [
  {
    id: "route-sj-fredericton",
    name: "Saint John → Fredericton (Route 7)",
    waypoints: [
      [45.2733, -66.0633], // Saint John
      [45.4667, -66.3667], // Welsford
      [45.85, -66.4761],   // Oromocto
      [45.9636, -66.6431], // Fredericton
    ],
  },
  {
    id: "route-moncton-saintjohn",
    name: "Moncton → Saint John (Route 1)",
    waypoints: [
      [46.0878, -64.7782], // Moncton
      [45.7185, -65.5138], // Sussex
      [45.2733, -66.0633], // Saint John
    ],
  },
  {
    id: "route-fredericton-edmundston",
    name: "Fredericton → Edmundston (TCH 2)",
    waypoints: [
      [45.9636, -66.6431], // Fredericton
      [46.1526, -67.5952], // Woodstock
      [47.0376, -67.7419], // Grand Falls
      [47.3735, -68.3251], // Edmundston
    ],
  },
  {
    id: "route-moncton-bathurst",
    name: "Moncton → Bathurst (Route 11/8)",
    waypoints: [
      [46.0878, -64.7782], // Moncton
      [47.0281, -65.5019], // Miramichi
      [47.6187, -65.6513], // Bathurst
    ],
  },
];

export function findRoute(routeId) {
  const route = ROUTES.find((r) => r.id === routeId);
  if (!route) throw new Error(`Unknown route: ${routeId}`);
  return route;
}
