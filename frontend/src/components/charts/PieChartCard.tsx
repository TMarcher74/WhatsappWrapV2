import { Card, CardContent } from "../ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

const COLORS = ["#4ade80", "#60a5fa", "#f472b6", "#facc15", "#fb923c"];

export default function PieChartCard({ data, title }: any) {
  return (
    <Card className="bg-neutral-900 border-neutral-700 p-4">
      <h2 className="text-xl mb-4">{title}</h2>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="label"
              fill="#8884d8"
              label
            >
              {data.map((_: any, index: number) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
