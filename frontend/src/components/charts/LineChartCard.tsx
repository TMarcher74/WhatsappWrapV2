import { Card, CardContent } from "../ui/card";
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from "recharts";

export default function LineChartCard({ data, title }: any) {
  return (
    <Card className="bg-neutral-900 border-neutral-700 p-4">
      <h2 className="text-xl mb-4">{title}</h2>
      <CardContent>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={data}>
            <XAxis dataKey="label" stroke="#fff" />
            <YAxis stroke="#fff" />
            <Line type="monotone" dataKey="value" stroke="#4ade80" />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
