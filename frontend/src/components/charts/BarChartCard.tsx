import { Card, CardContent } from "../ui/card";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from "recharts";

export default function BarChartCard({ data, title }: any) {
  return (
    <Card className="bg-neutral-900 border-neutral-700 p-4">
      <h2 className="text-xl mb-4">{title}</h2>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={data}>
            <XAxis dataKey="label" stroke="#fff" />
            <YAxis stroke="#fff" />
            <Bar dataKey="value" fill="#4ade80" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
